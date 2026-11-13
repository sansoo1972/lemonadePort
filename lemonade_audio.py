"""Own one audio player for as long as the game's stdin pipe stays open.

Launched privately by Speaker, not a persistent audio service. A closed pipe
means the game exited (including SIGKILL); then the player is terminated.
"""
from __future__ import annotations

import signal
import os
import subprocess
import sys
import threading
import time


def play_owned(command, duration, owner_pipe):
    stopped = threading.Event()

    def owner_closed():
        try:
            # Unbuffered reads avoid a daemon thread holding stdin's Python
            # buffered-reader lock when a short sound finishes normally.
            while os.read(owner_pipe.fileno(), 1):
                pass
        except OSError:
            pass
        finally:
            stopped.set()

    def stop_requested(signum, frame):
        stopped.set()

    handlers = {}
    for name in ('SIGTERM', 'SIGHUP', 'SIGINT'):
        sig = getattr(signal, name, None)
        if sig is not None:
            handlers[sig] = signal.signal(sig, stop_requested)
    player = None
    try:
        threading.Thread(target=owner_closed, daemon=True).start()
        if stopped.is_set():
            return 0
        player = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic() + max(1, duration) + 2
        while not stopped.wait(.05):
            result = player.poll()
            if result is not None:
                return result
            if time.monotonic() >= deadline:
                break
        return 0
    finally:
        if player is not None:
            if player.poll() is None:
                player.terminate()
            try:
                player.wait(timeout=.5)
            except subprocess.TimeoutExpired:
                player.kill()
                player.wait()
        for sig, handler in handlers.items():
            signal.signal(sig, handler)


def main():
    # All arguments are supplied by Speaker without a shell.
    if len(sys.argv) != 4:
        return 2
    try:
        return play_owned([sys.argv[1], sys.argv[2]], float(sys.argv[3]), sys.stdin.buffer)
    except (OSError, ValueError):
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
