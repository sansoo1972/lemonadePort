"""Centered terminal presentation and synthesized Apple-style speaker audio.

No third-party dependencies. Game rules live in lemonade_stand.py.
"""
from __future__ import annotations

from array import array
import atexit
from collections import deque
import os
import math
from pathlib import Path
import select
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import wave

# Literal title rows from BASIC 11110-11270. L is the green background;
# semicolons form the lettering in the Apple character-set trick.
TITLE_ROWS = (
    ";LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL;LLLLL",
    ";LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL;LLLLL",
    ";LLLL;;;;L;;;;;L;;;;L;;;;L;;;;L;;;;L;;;;",
    ";LLLL;LL;L;L;L;L;LL;L;LL;LLLL;L;LL;L;LL;",
    ";LLLL;;;;L;L;L;L;LL;L;LL;L;;;;L;LL;L;;;;",
    ";LLLL;LLLL;L;L;L;LL;L;LL;L;LL;L;LL;L;LLL",
    ";;;;L;;;;L;LLL;L;;;;L;LL;L;;;;L;;;;L;;;;",
    "",
    "LLLLLLLL;;;;;LL;LLLLLLLLLLLLLLL;LLLLLLLL",
    "LLLLLLLL;LLLLLL;LLLLLLLLLLLLLLL;LLLLLLLL",
    "LLLLLLLL;LLLLL;;;L;;;;L;;;;L;;;;LLLLLLLL",
    "LLLLLLLL;;;;;LL;LLLLL;L;LL;L;LL;LLLLLLLL",
    "LLLLLLLLLLLL;LL;LL;;;;L;LL;L;LL;LLLLLLLL",
    "LLLLLLLLLLLL;LL;LL;LL;L;LL;L;LL;LLLLLLLL",
    "LLLLLLLL;;;;;LL;LL;;;;L;LL;L;;;;LLLLLLLL",
)
TITLE = tuple(row.replace('L', ' ').replace(';', '#') for row in TITLE_ROWS)

# Original pitch/duration DATA pairs (11510, 11530-11560), zero terminators omitted.
TUNES = {
    'intro': ((96,180),(128,60),(114,60),(128,120),(144,60),(152,60),
              (128,255),(128,60),(114,60),(85,120),(96,60),(102,60),
              (114,120),(102,60),(96,255)),
    'sunny': ((96,16),(85,4),(128,4),(96,4),(76,4),(128,4),(96,16)),
    'hot': ((114,120),(144,60),(114,255),(1,120),(128,120),(144,60),
            (128,120),(114,60),(144,120),(171,255),(228,255)),
    'cloudy': ((152,180),(152,120),(152,60),(144,120),(152,60),
               (171,120),(192,60),(152,255)),
    'storm': ((0,160),(128,255),(152,40),(171,80),(192,40),(228,255),
              (1,40),(0,160),(192,255),(192,40),(171,80),(152,40),(128,255)),
    'report': ((152,80),(128,160),(152,40),(144,80),(128,200)),
}


def synthesize(notes, sample_rate=22050, tempo=0.55):
    """Approximate CALL 770's pitch delays with a quiet square-wave speaker.

    The original duration byte counts 256 inner-loop iterations per unit.
    A pitch of zero means an 8-bit counter wrapping through 256, not silence;
    pitch 1 is used by the weather routines for a rest.
    """
    if tempo <= 0:
        raise ValueError('Tempo must be positive')
    samples = array('h')
    for pitch, duration in notes:
        counter = pitch or 256
        frequency = 1_023_000 / (2 * (5 * counter + 14))
        seconds = duration * 256 * (5 + 14 / counter) / 1_023_000
        if pitch == 1:
            seconds = duration * .001
        count = max(1, int(seconds * sample_rate / tempo))
        for i in range(count):
            # A short envelope avoids harsh clicks between notes.
            release = max(80, int(.018 * sample_rate))
            envelope = min(1.0, i / 100, max(0, count - 1 - i) / release)
            amplitude = 1700 if (int(i * frequency * 2 / sample_rate) % 2 == 0) else -1700
            samples.append(0 if pitch == 1 else int(amplitude * envelope))
    if sys.byteorder != 'little':
        samples.byteswap()
    return samples.tobytes()


MELODY_SECONDS = len(synthesize(TUNES['intro'])) / (22050 * 2)


# One score for sound and animation: finish the melody, then six identical
# droplets at a steady rhythm. Neither timing nor pitch uses randomness.
DRIP_TIMES = tuple(MELODY_SECONDS + .3 + index * .6 for index in range(6))
OPENING_SECONDS = DRIP_TIMES[-1] + .9


def opening_audio(sample_rate=22050):
    """Slow title melody with soft, descending water drops and resonant plips."""
    music = array('h')
    music.frombytes(synthesize(TUNES['intro'], sample_rate))
    if sys.byteorder != 'little':
        music.byteswap()
    mixed = [int(value * .65) for value in music]
    mixed += [0] * max(0, int(OPENING_SECONDS * sample_rate) - len(mixed))
    for start in DRIP_TIMES:
        offset = int(start * sample_rate)
        phase = 0.0
        for i in range(int(.32 * sample_rate)):
            t = i / sample_rate
            frequency = 500 + 1700 * math.exp(-t * 23)
            phase += 2 * math.pi * frequency / sample_rate
            envelope = min(1, t / .004) * math.exp(-t * 19)
            drop = math.sin(phase) + .3 * math.sin(phase * 2.3)
            if offset + i < len(mixed):
                mixed[offset + i] += int(4300 * envelope * drop)
    samples = array('h', (max(-32768, min(32767, value)) for value in mixed))
    if sys.byteorder != 'little':
        samples.byteswap()
    return samples.tobytes()


def write_wav(path, pcm):
    with wave.open(str(path), 'wb') as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(22050)
        sound.writeframes(pcm)


class Speaker:
    """Generate local WAVs and play through an available system audio player."""
    def __init__(self, enabled=True):
        self.command = None
        if enabled:
            for name in ('afplay', 'aplay', 'paplay'):
                executable = shutil.which(name)
                if executable:
                    self.command = executable
                    break
        self.enabled = enabled and (self.command is not None or sys.platform == 'win32')
        self.directory = None
        self.process = None
        self.paths = {}
        self.ends_at = 0.0
        self.duration = 0.0

    def __enter__(self):
        if self.enabled:
            self.directory = tempfile.TemporaryDirectory(prefix='lemonade-audio-')
            atexit.register(self.stop)
        return self

    def play(self, name):
        if not self.enabled or self.directory is None:
            return
        self.wait()
        if not self.enabled:
            return
        try:
            if name not in self.paths:
                path = Path(self.directory.name) / f'{name}.wav'
                write_wav(path, opening_audio() if name == 'opening' else synthesize(TUNES[name]))
                self.paths[name] = path
            with wave.open(str(self.paths[name])) as sound:
                self.duration = sound.getnframes() / sound.getframerate()
            self.ends_at = time.monotonic() + self.duration
            if sys.platform == 'win32':
                import winsound
                winsound.PlaySound(str(self.paths[name]), winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                worker = Path(__file__).with_name('lemonade_audio.py')
                self.process = subprocess.Popen(
                    [sys.executable, str(worker), self.command, str(self.paths[name]), str(self.duration)],
                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True)
        except (OSError, RuntimeError):
            self.enabled = False

    def wait(self):
        """Let a cue finish; cleanup/interrupts can still stop it immediately."""
        if self.process is not None:
            try:
                result = self.process.wait(timeout=max(1, self.ends_at - time.monotonic() + 2))
                if result:
                    self.enabled = False
            except subprocess.TimeoutExpired:
                self.stop()
                self.enabled = False
            if self.process is not None and self.process.stdin is not None:
                self.process.stdin.close()
            self.process = None
        elif sys.platform == 'win32' and self.enabled:
            remaining = self.ends_at - time.monotonic()
            if remaining > 0:
                time.sleep(remaining)

    def stop(self):
        if self.process is not None:
            process, self.process = self.process, None
            # Closing the ownership pipe lets the worker stop its own player.
            if process.stdin is not None:
                process.stdin.close()
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        if sys.platform == 'win32' and self.enabled:
            import winsound
            winsound.PlaySound(None, 0)

    def __exit__(self, *exc):
        self.stop()
        atexit.unregister(self.stop)
        if self.directory is not None:
            self.directory.cleanup()
            self.directory = None


class CRT:
    """40-column phosphor text inside a dark, approximately 4:3 monitor.

    Terminal cells are assumed twice as tall as wide. Thus 8:3 in character
    coordinates is 4:3 physically; font aspect ratios vary by terminal.
    """
    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stdout
        self.lines = []
        self.prompt = ''
        self.answer = ''
        self.size = None
        self.active = False
        self.key_mode = False

    def __enter__(self):
        self.active = True
        self.stream.write('\x1b[?1049h\x1b[48;2;3;4;3m\x1b[38;5;120m\x1b[2J')
        self.stream.flush()
        self.render()
        return self

    def __exit__(self, *exc):
        self.active = False
        self.stream.write('\x1b[0m\x1b[?25h\x1b[?1049l')
        self.stream.flush()

    def clear(self):
        self.lines = []
        self.prompt = self.answer = ''
        self.render()

    def write(self, text):
        # Bound retained screen history; resizing can reflow recent text.
        self.lines.extend(str(text).split('\n'))
        self.lines = self.lines[-100:]
        self.render()

    @staticmethod
    def monitor_geometry(size):
        columns, rows = size
        height = max(3, min(36, rows - 2, int(max(8, columns - 4) * 3 / 8)))
        width = max(3, min(columns, round(height * 8 / 3)))
        height = min(rows, height)
        return width, height, max(0, (columns - width) // 2), max(0, (rows - height) // 2)

    @staticmethod
    def layout(lines, prompt='', answer='', size=(80, 30), key_mode=False):
        columns, rows = size
        monitor_width, monitor_height, _, _ = CRT.monitor_geometry(size)
        width = max(1, min(40, monitor_width - 6))
        height = max(1, min(24, monitor_height - 2))
        wrapped = []
        for line in lines:
            wrapped.extend(textwrap.wrap(line, width, replace_whitespace=False,
                                         drop_whitespace=True) or [''])
        if prompt:
            wrapped.extend(textwrap.wrap(prompt.rstrip(), width) or [''])
            # Keep typed characters on their own row inside the CRT screen.
            if not key_mode:
                wrapped.append('> ' + answer[-max(0, width - 3):])
        visible = list(deque(wrapped, maxlen=height))
        leading = (height - len(visible)) // 2
        visible = [''] * leading + visible
        visible += [''] * (height - len(visible))
        left = max(0, (columns - width - 2) // 2)
        top = max(0, (rows - height - 2) // 2)
        frame = ['+' + '-' * width + '+']
        frame += ['|' + line[:width].ljust(width) + '|' for line in visible]
        frame += ['+' + '-' * width + '+']
        return frame, top, left, width, height, leading + min(len(wrapped), height)

    def render(self):
        self.size = shutil.get_terminal_size((80, 30))
        frame, top, left, width, height, used = self.layout(
            self.lines, self.prompt, self.answer, self.size, self.key_mode)
        monitor_width, monitor_height, monitor_left, monitor_top = self.monitor_geometry(self.size)
        output = ['\x1b[?25l\x1b[48;2;3;4;3m\x1b[H\x1b[2J']
        # Low-contrast bezel: filled charcoal, not a bright box-drawing border.
        for row in range(monitor_height):
            output.append(f'\x1b[{monitor_top + row + 1};{monitor_left + 1}H'
                          '\x1b[48;2;17;20;18m' + ' ' * monitor_width)
        for row in range(max(0, monitor_height - 2)):
            output.append(f'\x1b[{monitor_top + row + 2};{monitor_left + 4}H'
                          '\x1b[48;2;0;3;1m' + ' ' * max(0, monitor_width - 6))
        output.append('\x1b[38;5;120m\x1b[48;2;0;3;1m')
        # Strip the logical layout border; the larger monitor provides the frame.
        for row, line in enumerate(frame[1:-1], top + 2):
            output.append(f'\x1b[{row};{left + 2}H{line[1:-1]}')
        if self.prompt and not self.key_mode:
            output.append(f'\x1b[{top + used + 1};{left + 4 + min(len(self.answer), max(0, width - 3))}H\x1b[?25h')
        self.stream.write(''.join(output))
        self.stream.flush()

    def ask(self, prompt):
        self.prompt, self.answer = prompt, ''
        self.render()
        try:
            answer = self._read_line()
        finally:
            self.prompt = ''
        # Retain the question/answer until the next page change.
        self.lines.extend(textwrap.wrap(prompt.rstrip(), 40))
        if not self.key_mode:
            self.lines.append('> ' + ('[ESC]' if answer == '\x1b' else answer))
        self.answer = ''
        self.render()
        return answer

    def wait_key(self, prompt):
        """Space/Return/Escape act immediately, without editing or echoing."""
        self.key_mode = True
        try:
            return self.ask(prompt)
        finally:
            self.key_mode = False

    def _read_line(self):
        if os.name == 'nt':
            import msvcrt
            def get_character():
                while not msvcrt.kbhit():
                    self._resize()
                    time.sleep(.05)
                char = msvcrt.getwch()
                if char in ('\x00', '\xe0'):
                    msvcrt.getwch()
                    return ''
                return char
            return self._edit(get_character)
        import termios
        import tty
        descriptor = sys.stdin.fileno()
        original = termios.tcgetattr(descriptor)
        try:
            tty.setcbreak(descriptor, termios.TCSANOW)
            def get_character():
                while not select.select([sys.stdin], [], [], .1)[0]:
                    self._resize()
                char = os.read(descriptor, 1).decode('ascii', errors='ignore')
                if char == '':
                    raise EOFError
                # Eat cursor/function key sequences; a bare ESC ends a pause.
                if char == '\x1b' and select.select([sys.stdin], [], [], .04)[0]:
                    suffix = os.read(descriptor, 1).decode('ascii', errors='ignore')
                    if suffix in ('[', 'O'):
                        while select.select([sys.stdin], [], [], .02)[0]:
                            tail = os.read(descriptor, 1).decode('ascii', errors='ignore')
                            if tail.isalpha() or tail == '~':
                                break
                        return ''
                return char
            return self._edit(get_character)
        finally:
            termios.tcsetattr(descriptor, termios.TCSADRAIN, original)

    def _edit(self, get_character):
        while True:
            char = get_character()
            if char in ('\r', '\n'):
                return '' if self.key_mode else self.answer
            if char == '\x1b':
                return char
            if char == '\x03':
                raise KeyboardInterrupt
            if char == '\x04':
                raise EOFError
            if self.key_mode:
                if char == ' ':
                    return ' '
                continue
            if char in ('\x7f', '\b'):
                self.answer = self.answer[:-1]
            elif char == '\x15':
                self.answer = ''
            elif char and char.isprintable() and len(self.answer) < 128:
                self.answer += char
            self.render()

    def _resize(self):
        if shutil.get_terminal_size((80, 30)) != self.size:
            self.render()

    @staticmethod
    def title_lines():
        return list(TITLE) + ['', 'LEMONADE STAND'.center(40),
                              'COPYRIGHT 1979 APPLE COMPUTER INC.'.center(40)]

    def opening(self):
        start = time.monotonic()
        # Keep the complete lettering visible as drops fall beneath STAND.
        while True:
            elapsed = time.monotonic() - start
            if elapsed >= OPENING_SECONDS:
                break
            rows = list(TITLE) + [' ' * 40 for _ in range(3)]
            for index, moment in enumerate(DRIP_TIMES):
                age = elapsed - moment
                if 0 <= age < .65:
                    x = (10, 20, 30, 14, 25, 34)[index]
                    y = 15 + min(2, int(age / .22))
                    row = list(rows[y])
                    row[x] = '.' if age < .5 else 'o'
                    rows[y] = ''.join(row)
            self.lines = rows + ['', 'LEMONADE STAND'.center(40)]
            self.render()
            time.sleep(.06)
        self.lines = self.title_lines()
        self.render()

    def weather(self, weather):
        self.clear()
        # The same 40 x 40 low-resolution coordinates as BASIC 15110-15162,
        # packed two pixels high into each terminal character.
        pixels = [[int(weather) if y <= 25 else 12 for _ in range(40)] for y in range(40)]
        def hline(x1, x2, y, color):
            for x in range(x1, x2 + 1):
                pixels[y][x] = color
        def vline(y1, y2, x, color):
            for y in range(y1, y2 + 1):
                pixels[y][x] = color
        for y in range(24, 33):
            hline(15, 25, y, 8)
        for y in range(17, 24, 2):
            vline(22, 23, y, 13)
        if int(weather) in (2, 7):
            color = 15 if int(weather) == 2 else 9
            hline(3, 5, 1, color)
            for y in range(2, 7):
                hline(2, 6, y, color)
            hline(3, 5, 8, color)
        else:
            color = 15 if int(weather) == 10 else 0
            for x1, x2, y in ((6,10,2),(4,14,3),(7,12,4),(22,30,4),(20,36,5),(23,33,6)):
                hline(x1,x2,y,color)
            if int(weather) == 5:
                for y1,y2,x in ((7,9,29),(9,14,32),(14,25,35),(5,8,8),(8,13,10),(13,17,12)):
                    vline(y1,y2,x,10)
                hline(30,31,9,10)
                hline(33,34,14,10)
        # A monochrome CRT interpretation: sky is dark, ground shaded,
        # sun/clouds bright, cart brown/pink shapes become solid silhouettes.
        shades = {0:' ', 2:' ', 5:' ', 7:' ', 8:'#', 9:'@',
                  10: '/' if int(weather) == 5 else ' ', 12:'.', 13:'#', 15:'@'}
        self.lines = [''.join(shades.get(pixels[y][x], '#') for x in range(40))
                      for y in range(0, 40, 2)]
        self.render()
        time.sleep(.9)
