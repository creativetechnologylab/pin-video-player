from os import path
import logging
import time
import atexit
import pygame

try:
    import pigpio
    pi = pigpio.pi()
except ModuleNotFoundError:
    logging.error('No pigpio, are you running on a Pi?')
    class Pi:
        def callback(*args, **kwargs):
            pass
    class pigpio:
        FALLING_EDGE = None
    pi = Pi()

import omx

class NoPinException(Exception):
    pass

class BadAssetException(Exception):
    pass

class Player:
    
    def __init__(self, pin_map):

        pygame.init()
        pygame.mouse.set_visible(False)
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.load(pin_map)
        
        for bcm, video in self.pins.items():
            pi.set_mode(bcm, pigpio.INPUT)
            pi.set_pull_up_down(bcm, pigpio.PUD_UP)
            pi.callback(bcm, pigpio.FALLING_EDGE, self.__gpio_change)

    @atexit.register
    def cleanup():
        pygame.quit()



    def load(self, pin_map):
        self.pins = {}
        
        for e in pin_map:
            if 'bcm' in e:
                bcm = e['bcm']
            elif 'gpio' in e:
                bcm = gpio2bcm(e['gpio'])
            else:
                raise NoPinException('Error in pin map, either specify a bcm or gpio pin')

            try:
                asset = {
                    'image': pygame.image.load(e['image']),
                }
                image = path.basename(e['image'])
                logging.info('added {}'.format(image))


                if 'video' in e:
                    asset['video'] = e['video']
                    video = path.basename(e['video'])
                    logging.info('added {}'.format(video))


                self.pins[bcm] = asset

                
            except AttributeError:
                raise BadAssetException('{}'.format(e))

    def wait_for_key(self):
        clock = pygame.time.Clock()
        alive = True
        while alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    alive = False

            clock.tick(1)
                
        
    def __gpio_change(self, bcm, level, t):
        if hasattr(self, 'last_update'):
            if time.time() - self.last_update < 2:
                return
        
        if bcm in self.pins:
            asset = self.pins[bcm]

            if 'video' in asset:
                omx.play(asset['video'])

            time.sleep(1)
            self.surface.blit(asset['image'], (0, 0))
            pygame.display.update()
            logging.info('dislaying {}'.format(asset['image']))


        self.last_update = time.time()
