"""Presentation checks: original data, fitting, input editing, WAVs and cleanup."""
import io
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import wave

from lemonade_crt import CRT, Speaker, TITLE_ROWS, TUNES, synthesize, opening_audio, OPENING_SECONDS, DRIP_TIMES, MELODY_SECONDS


class CRTTests(unittest.TestCase):
    def test_title_rows_match_basic_listing(self):
        source = Path(__file__).resolve().parents[1] / 'lemonade_stand.basic'
        rows = []
        for line in source.read_text().splitlines():
            if re.match(r'111[1-7]0 |112[1-7]0 ', line):
                rows.append(re.search(r'PRINT "([^"]*)"', line).group(1))
        self.assertEqual(rows, list(TITLE_ROWS[:7] + TITLE_ROWS[8:]))

    def test_original_melodies_match_data(self):
        source = Path(__file__).resolve().parents[1] / 'lemonade_stand.basic'
        for number, name in [(11510,'intro'), (11530,'sunny'), (11540,'hot'),
                             (11550,'cloudy'), (11560,'storm')]:
            line = next(line for line in source.read_text().splitlines() if line.startswith(str(number)))
            values = [int(item) for item in line.split('DATA')[1].split(',')]
            self.assertEqual(list(TUNES[name]), list(zip(values[0:-2:2], values[1:-2:2])))

    def test_screen_centering_and_bounds(self):
        for columns, rows in [(120, 50), (80, 30), (80, 24), (40, 20), (20, 10)]:
            frame, top, left, width, height, _ = CRT.layout(
                ['HELLO ' * 20], 'WHAT PRICE?', '123', (columns, rows))
            self.assertLessEqual(left + len(frame[0]), columns)
            self.assertLessEqual(top + len(frame), rows)
            self.assertLessEqual(abs(left - (columns - left - len(frame[0]))), 1)
            self.assertLessEqual(abs(top - (rows - top - len(frame))), 1)
            self.assertEqual(len(frame), height + 2)
            self.assertTrue(all(len(line) == width + 2 for line in frame))

    def test_long_input_stays_in_frame(self):
        frame, *_ = CRT.layout(['REPORT'], 'INPUT', '9' * 128, (80, 30))
        self.assertTrue(all(len(line) == 42 for line in frame))
        self.assertIn('> ', '\n'.join(frame))

    def test_monitor_is_larger_than_text_with_four_three_proportions(self):
        for size in [(120, 50), (80, 30), (80, 24)]:
            width, height, left, top = CRT.monitor_geometry(size)
            self.assertAlmostEqual(width / (height * 2), 4 / 3, delta=.025)
            self.assertGreater(width, 42)
            self.assertLessEqual(left + width, size[0])
            self.assertLessEqual(top + height, size[1])

    def test_music_slows_without_changing_sample_rate(self):
        fast = synthesize(TUNES['intro'], tempo=1)
        slow = synthesize(TUNES['intro'])
        self.assertAlmostEqual(len(slow) / len(fast), 1 / .55, places=3)
        with self.assertRaises(ValueError):
            synthesize(TUNES['intro'], tempo=0)

    def test_opening_contains_drips_after_melody_ends(self):
        from array import array
        pcm = opening_audio()
        self.assertEqual(len(pcm), int(OPENING_SECONDS * 22050) * 2)
        samples = array('h')
        samples.frombytes(pcm)
        self.assertTrue(any(samples[int(4.85 * 22050):int(5.1 * 22050)]))
        self.assertLess(max(abs(value) for value in samples), 10000)

    def test_title_animation_ends_with_complete_title(self):
        screen = CRT(io.StringIO())
        with patch('lemonade_crt.time.monotonic', side_effect=[0, 0, 1, OPENING_SECONDS + 1]), \
             patch('lemonade_crt.time.sleep'):
            screen.opening()
        self.assertEqual(screen.lines, CRT.title_lines())
        self.assertIn('LEMONADE STAND', '\n'.join(screen.lines))

    def test_space_continues_without_return_or_echo(self):
        screen = CRT(io.StringIO())
        characters = iter('x ')
        with patch.object(screen, '_read_line', side_effect=lambda: screen._edit(lambda: next(characters))):
            self.assertEqual(screen.wait_key('PRESS SPACE'), ' ')
        self.assertEqual(screen.answer, '')
        self.assertFalse(screen.key_mode)
        self.assertFalse(any(line.startswith('>') for line in screen.lines))

    def test_escape_ends_key_prompt_and_restores_input_mode(self):
        screen = CRT(io.StringIO())
        with patch.object(screen, '_read_line', side_effect=lambda: screen._edit(lambda: '\x1b')):
            self.assertEqual(screen.wait_key('CONTINUE'), '\x1b')
        self.assertFalse(screen.key_mode)
        with patch.object(screen, '_read_line', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                screen.wait_key('CONTINUE')
        self.assertFalse(screen.key_mode)

    def test_spaces_still_work_in_normal_text(self):
        screen = CRT(io.StringIO())
        characters = iter('A B\r')
        self.assertEqual(screen._edit(lambda: next(characters)), 'A B')

    def test_drips_follow_melody_and_have_even_timing(self):
        self.assertGreater(DRIP_TIMES[0], MELODY_SECONDS)
        for first, second in zip(DRIP_TIMES, DRIP_TIMES[1:]):
            self.assertAlmostEqual(second - first, .6)
        self.assertEqual(opening_audio(), opening_audio())

    def test_sound_cues_finish_before_next_player_starts(self):
        events = []
        with patch('lemonade_crt.shutil.which', return_value='/usr/bin/afplay'), \
             patch('lemonade_crt.subprocess.Popen') as process:
            process.side_effect = lambda *a, **kw: events.append('play') or player
            from unittest.mock import Mock
            player = Mock()
            player.wait.side_effect = lambda **kw: events.append('finish') or 0
            player.poll.return_value = 0
            with Speaker() as speaker:
                speaker.play('intro')
                speaker.play('report')
            self.assertEqual(events[:3], ['play', 'finish', 'play'])
            player.terminate.assert_not_called()

    def test_input_editing_and_escape(self):
        screen = CRT(io.StringIO())
        chars = iter('123\x7f4\r')
        self.assertEqual(screen._edit(lambda: next(chars)), '124')
        self.assertEqual(screen._edit(lambda: '\x1b'), '\x1b')
        with self.assertRaises(EOFError):
            screen._edit(lambda: '\x04')

    def test_escape_answer_is_not_written_as_terminal_control(self):
        screen = CRT(io.StringIO())
        with patch.object(screen, '_read_line', return_value='\x1b'):
            self.assertEqual(screen.ask('CONTINUE?'), '\x1b')
        self.assertEqual(screen.lines[-1], '> [ESC]')

    def test_terminal_restored_on_exception(self):
        stream = io.StringIO()
        with self.assertRaises(RuntimeError):
            with CRT(stream):
                raise RuntimeError('test')
        output = stream.getvalue()
        self.assertIn('\x1b[?1049h', output)
        self.assertTrue(output.endswith('\x1b[0m\x1b[?25h\x1b[?1049l'))

    def test_all_tunes_produce_valid_audio(self):
        for notes in TUNES.values():
            pcm = synthesize(notes)
            self.assertGreater(len(pcm), 100)
            self.assertEqual(len(pcm) % 2, 0)
            output = io.BytesIO()
            with wave.open(output, 'wb') as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(22050)
                wav.writeframes(pcm)
            with wave.open(io.BytesIO(output.getvalue())) as wav:
                self.assertEqual(wav.getnframes(), len(pcm) // 2)

    def test_muted_audio_does_not_start_process_or_make_files(self):
        with patch('lemonade_crt.subprocess.Popen') as process:
            with Speaker(enabled=False) as speaker:
                speaker.play('intro')
                self.assertIsNone(speaker.directory)
            process.assert_not_called()

    def test_player_files_and_process_are_cleaned_up(self):
        with patch('lemonade_crt.shutil.which', return_value='/usr/bin/afplay'), \
             patch('lemonade_crt.subprocess.Popen') as process:
            process.return_value.poll.return_value = None
            with Speaker() as speaker:
                speaker.play('intro')
                path = speaker.paths['intro']
                self.assertTrue(path.exists())
                with wave.open(str(path)) as wav:
                    self.assertEqual(wav.getnchannels(), 1)
            self.assertFalse(path.exists())
            process.return_value.stdin.close.assert_called_once()
            process.return_value.terminate.assert_not_called()
            process.return_value.wait.assert_called_once()


if __name__ == '__main__':
    unittest.main()
