import subprocess
import logging
import threading

thread = None
running = threading.Event()

def play(path):
    global thread
    if not running.is_set():
        thread = threading.Thread(target=_play, args=(path,))
        thread.start()
    else:
        logging.warning('not playing video, as one is already playing')

def _play(path):
    logging.info('omxplayer {}'.format(path))
    running.set()
    p = subprocess.run(['omxplayer', path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    running.clear()
    logging.info('finished video')
