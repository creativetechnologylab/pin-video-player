#!/usr/bin/env python3
"""
pin-video-player.py

Usage:
  pin-video-player.py <pin-map>
  pin-video-player.py (-h | --help)
  pin-video-player.py --version

Options:
  -h --help        Show this screen
  --version        Show version
"""
import logging
import yaml
from docopt import docopt

from player import Player

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    args = docopt(__doc__, version=0.1)
    pin_map = yaml.load(open(args['<pin-map>']))
    player = Player(pin_map)

    try:
        player.wait_for_key()
    except KeyboardInterrupt:
        pass

    
    
