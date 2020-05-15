import pygame as pg
from data.classes.settings import *
class ScoreKeeperTop(pg.sprite.Sprite):
    ''' This class defines the scoreboard in where you keep track of the status of the player '''
    
    def __init__(self, game):
        ''' Initalizer takes the screen surface parameters to set location of the scorekeeper '''
        
        #Adds to all sprite group
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Call the sprite __init__() method
        pg.sprite.Sprite.__init__(self)

        # Sets the font used for the sprite
        self.font = pg.font.Font('data/font/arcade.ttf', 16)
        
        # Set instance variables used to track score
        self.currentLevel = 0
        self.completeTiles = 0
        self.totalTiles = 0
        self.solvedLevels = 0
        self.playerMelted = 0
        # The text that contains the score that constantly update
        self.message = ""
        self.image = self.font.render(self.message, 1, (0, 0, 0))
        
        # Set the position of the sprites
        
        self.rect = self.image.get_rect()
        self.rect.centery = TILESIZE - 15
        
        self.message = " "
        
        # Variable just used for keeping track of the game
        self.game = game
                    
    def checkFinish(self):
        ''' This method checks if the player has finished the level by passing all tiles '''
        return (self.completeTiles == self.totalTiles)      
          
    def update(self):
        '''This method will be called automatically to display 
        the game information at the top of the game window.'''
 
        # The text that contains the information that constantly update
        self.message = "%11s%3d%20d%s%-20d%s%3d" % ( "LEVEL", self.currentLevel, self.completeTiles,\
                                                                               "/", self.totalTiles, "SOLVED", self.solvedLevels)
        self.image = self.font.render(self.message, 1, (0, 0, 0))