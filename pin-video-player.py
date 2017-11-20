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

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":

    args = docopt(__doc__, version=0.1)
    # yaml.load(pin_map_path)
    pin_map = yaml.load(open(args['<pin-map>']))
    print(pin_map)
    player = Player(pin_map)

    _ = input()
    
