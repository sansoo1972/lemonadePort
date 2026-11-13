"""Real subprocess checks with a silent fake player; no device/audio required."""
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


WORKER = Path(__file__).resolve().parents[1] / 'lemonade_audio.py'


class AudioLifecycleTests(unittest.TestCase):
    def wait_for_file(self, path):
        deadline = time.monotonic() + 4
        while not path.exists() and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertTrue(path.exists(), f'{path.name} was not created')

    def fake_player(self, directory):
        path = Path(directory) / 'silent_player.py'
        path.write_text('''from pathlib import Path
import signal, time
base = Path(__file__).parent
(base / 'started').touch()
def stop(*args):
    (base / 'stopped').touch()
    raise SystemExit(0)
signal.signal(signal.SIGTERM, stop)
while True:
    time.sleep(.05)
''')
        return path

    def test_closing_owner_pipe_stops_audio_player(self):
        with tempfile.TemporaryDirectory() as directory:
            player = self.fake_player(directory)
            worker = subprocess.Popen([sys.executable, str(WORKER), sys.executable, str(player), '30'],
                                      stdin=subprocess.PIPE)
            try:
                self.wait_for_file(Path(directory) / 'started')
                worker.stdin.close()
                self.assertEqual(worker.wait(timeout=3), 0)
                self.assertTrue((Path(directory) / 'stopped').exists())
            finally:
                if worker.poll() is None:
                    worker.terminate()
                    worker.wait(timeout=3)
                if not worker.stdin.closed:
                    worker.stdin.close()

    def test_killing_game_owner_stops_audio_without_exit_handlers(self):
        with tempfile.TemporaryDirectory() as directory:
            player = self.fake_player(directory)
            code = '''import subprocess, sys, time
subprocess.Popen([sys.executable, sys.argv[1], sys.executable, sys.argv[2], '30'],
                 stdin=subprocess.PIPE, start_new_session=True)
time.sleep(30)
'''
            owner = subprocess.Popen([sys.executable, '-c', code, str(WORKER), str(player)])
            try:
                self.wait_for_file(Path(directory) / 'started')
                owner.kill()  # No finally/atexit cleanup can run in the owner.
                owner.wait(timeout=3)
                self.wait_for_file(Path(directory) / 'stopped')
            finally:
                if owner.poll() is None:
                    owner.kill()
                    owner.wait(timeout=3)

    def test_short_player_finishes_without_waiting_for_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            player = Path(directory) / 'short_player.py'
            player.write_text('pass\n')
            worker = subprocess.Popen([sys.executable, str(WORKER), sys.executable, str(player), '1'],
                                      stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                self.assertEqual(worker.wait(timeout=3), 0)
                self.assertEqual(worker.stderr.read(), b'')
            finally:
                if worker.poll() is None:
                    worker.terminate()
                    worker.wait(timeout=3)
                worker.stdin.close()
                worker.stderr.close()
