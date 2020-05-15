import pygame as pg
from data.classes.settings import *
class Unused(pg.sprite.Sprite):
    ''' This class represents an unused tile in game '''
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("data/images/unused.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.image.set_colorkey((0,0,0))