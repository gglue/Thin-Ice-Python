import pygame as pg
from data.classes.settings import *
class ScoreKeeperBottom(pg.sprite.Sprite):
    ''' This class defines the scoreboard in where you keep track of the current score '''
    
    def __init__(self, game):
        ''' Initalizer takes the screen surface parameters to set location of the scorekeeper '''
        
        #Adds to all sprite group
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Call the sprite __init__() method
        pg.sprite.Sprite.__init__(self)

        # Sets the font used for the sprite
        self.font = pg.font.Font('data/font/arcade.ttf', 16)
        
        # Keeps track of the score
        self.score = 0
        
        # Previous score from last stage
        self.previousScore = 0;
        
        # The text that contains the score that constantly update
        self.message = "POINTS %-4d" % self.score
        self.image = self.font.render(self.message, 1, (0, 0, 0))        
        
        # Set the position of the sprites
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT - 12
        self.rect.centerx = WIDTH - TILESIZE * 3
            
    def update(self):
        '''This method will be called automatically to display 
        the game information at the bottom of the game window.'''
        
        # The text that contains the score that constantly update
        self.message = "POINTS %-4d" % self.score
        self.image = self.font.render(self.message, 1, (0, 0, 0))