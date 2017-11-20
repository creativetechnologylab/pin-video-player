import subprocess
import os
import signal
import atexit
import json
import logging
import requests

class NoPlaylistItemException(Exception):
    pass

class VLC:
    pid = None

    # singleton pattern
    _instance = None
    def __new__(cls):
        if VLC._instance is None:
            VLC._instance = object.__new__(cls)
        return VLC._instance
    
    def __init__(self):
        self.vlc = subprocess.Popen(['vlc'])
        VLC.pid = self.vlc.pid
        logging.info('opened VLC ({})'.format(VLC.pid))

        self.auth = ('', 's')
        
    @atexit.register
    def cleanup():
        if VLC.pid != None:
            os.kill(VLC.pid, signal.SIGTERM)
        

    def _control(self, command, **kwargs):
        endpoint = 'http://localhost:8080/requests/status.json'
        params = {
            'command': command
        }

        params.update(kwargs)

        requests.get(endpoint, params=params, auth=self.auth)


    def add(self, path):
        self._control('in_enqueue', input=path)
        self.update_playlist()
        
    def play(self, name):

        if name not in self.playlist:
            self.update_playlist()
        
        try:
            id = self.playlist[name]
            self._control('pl_play', id=id)
            logging.info('playing {} ({})'.format(name, id))
        except AttributeError:
            raise NoPlaylistItemException('Item not in playlist')
    
    def update_playlist(self):
        r = requests.get('http://localhost:8080/requests/playlist.json', auth=self.auth)
        d = json.loads(r.text)
        playlist = d['children'][0]['children']

        self.playlist = { e['name']: e['id'] for e in playlist }
        
        logging.info('updated playlist, {} items'.format(len(self.playlist)))
        
