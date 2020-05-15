import pygame as pg
from data.classes.settings import *
class noWaterTile(pg.sprite.Sprite):
    ''' This class defines a tile where water will not be created when the player leaves the tile '''
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.noWaterGroup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class MovingBlockTile(noWaterTile):
    ''' This class defines a tile that indicates the location of where the moving block should be in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/movingBlockTile.png")
        self.image.set_colorkey((255,255,255))
              
class Teleporter(noWaterTile):
    ''' This class defines a tile that teleports you to another teleporter  '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.currentFrame = 1
        self.image = self.game.teleporterSpriteSheet.get_image(self.currentFrame)
             
    def update(self):
        '''Updates the player sprite '''
        
        if self.currentFrame < 21 and self.game.canTeleport == True:
            self.currentFrame += 1
            
        self.image = self.game.teleporterSpriteSheet.get_image(self.currentFrame)
            
        if self.currentFrame >= 21 and self.game.canTeleport == True:
            self.currentFrame = 1
            
        if not self.game.canTeleport:
            self.currentFrame = 22