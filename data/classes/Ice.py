import pygame as pg
from data.classes.settings import *
class Ice(pg.sprite.Sprite):
    ''' This class represents an ice tile in game '''
    
    def __init__(self, game, x, y):
        self.groups = game.iceSprites, game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("data/images/ice.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE