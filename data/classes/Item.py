import pygame as pg
from data.classes.settings import *

class Item(pg.sprite.Sprite):
    ''' This class represents sprites that can be picked up 
    by the user'''
    
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Treasure(Item):
    ''' This class represents the treasure bag in the game, which
    is only spawned if they solved the previous level'''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/treasure.png")
        self.image.set_colorkey((255,255,255))
        
        
class GoldenKey(Item):
    '''  This class represents a key used in the game to unlock a socket '''
    
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.currentFrame = 1
        self.image = self.game.keySpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        

    def update(self):
        '''Updates the player sprite '''
        
        self.currentFrame += 1
        
        self.image = self.game.keySpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        
        # Never play initial animation after creation
        if self.currentFrame == 32:
            self.currentFrame = 1