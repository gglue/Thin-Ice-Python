import pygame as pg
from data.classes.settings import *
class Immovable(pg.sprite.Sprite):
    ''' This class represents a tile in the game that you won't be able to move through '''
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class KeyHole(Immovable):
    ''' This class represents a key socket tile that can be opened when the player has a key '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/socket.png")
        
class Wall(Immovable):
    ''' This class represents a wall in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/wall.png")
        
class Water(Immovable):
    ''' This class represents a water block in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.currentFrame = 1
        self.image = self.game.waterSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey((255,255,255))        

    def update(self):
        '''Updates the player sprite '''
        
        self.currentFrame += 1
        
        self.image = self.game.waterSpriteSheet.get_image(self.currentFrame)
        
        # Never play initial animation after creation
        if self.currentFrame == 39:
            self.currentFrame = 7
