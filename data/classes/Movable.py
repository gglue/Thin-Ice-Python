import pygame as pg
from data.classes.settings import *
class Movable(pg.sprite.Sprite):
    ''' This class represents a tile in the game that you will be able to move through '''
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.movable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Free(Movable):
    ''' This class represents a free tile in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/free.png")
        self.image.set_colorkey((255,255,255))
        
class End(Movable):
    ''' This class represents the finish line in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/finish.png")
        self.image.set_colorkey((255,255,255))