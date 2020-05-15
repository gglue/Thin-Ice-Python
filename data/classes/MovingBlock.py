import pygame as pg
from data.classes.settings import *
class MovingBlock(pg.sprite.Sprite):
    ''' This class defines a block that is pushed by the player '''
    
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.updatingBlockGroup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("data/images/movingBlock.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.image.set_colorkey((0,0,0))
        
        self.dx = 0
        self.dy = 0
        
        self.game = game

    def collideWithWalls(self):
        ''' This method checks if the block has collison with any walls '''
        # Checks all the wall entities
        for wall in self.game.walls:
            
            if wall.x == self.x + self.dx and wall.y == self.y + self.dy:
                self.game.blockIsMoving = False
                return True
               
        # Allow block to move if theres nothing in the way    
        return False
        
    def move(self, dx = 0, dy = 0):
        ''' This function moves the block '''
        self.x += dx
        self.y += dy

    def collideWithTile(self, tile):
        ''' This method checks if the player is in the same tile as the parameter '''
        
        # True if on the same tile
        if tile.x == self.x and tile.y == self.y:
            return True
        else:
            return False
        
    def setVelocity(self, dx, dy):
        ''' This function sets the velocity of the block '''
        self.game.movingBlockSound.play()
        self.dx = dx
        self.dy = dy
        
    def movetoCoordinate(self, x, y):
        ''' This method moves the player to a specific coordinate '''
        self.x = x
        self.y = y
        
    def update(self):
        ''' This method updates the blocks' position '''
        
        tempBoolean = self.collideWithWalls()
        
        # Move the block if the game says the block is moving
        if not tempBoolean and self.game.blockIsMoving:
            self.move(self.dx, self.dy)

        # Teleport if it touches a teleporter
        if self.game.currentLevel > TELEPORTLEVEL:
            if self.collideWithTile(self.game.secondTeleporter):
                if self.game.canTeleport:
                    self.game.movingBlock.movetoCoordinate(self.game.firstTeleporter.x, self.game.firstTeleporter.y)
                    self.game.teleportSound.play()        
            
        # Updates the position
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
