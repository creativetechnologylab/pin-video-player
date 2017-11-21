import subprocess
import logging
import threading

thread = None

def play(path):
    global thread
    thread = threading.Thread(target=_play, args=(path,))
    thread.start()

def _play(path):
    logging.info('omxplayer {}'.format(path))
    subprocess.run(['omxplayer', path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
