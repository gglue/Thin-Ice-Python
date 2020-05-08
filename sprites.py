'''
Name: Victor Li
Date: 5/7/2020
Description: Classes used for the main program
'''

# Importing used classes
import pygame as pg
import xml.etree.ElementTree as ET
from settings import *

class Spritesheet:
    '''This class is used to grab smaller sprites from spritesheets '''
    
    def __init__(self, filename):
        '''This initializer takes the file name as a parameter to load'''
        
        #Loads the PNG file
        self.spritesheet = pg.image.load(filename).convert()
        
        #Loads the XML file
        self.xml = ET.parse(PLAYERXML)
        self.root = self.xml.getroot() 
        
        #Variable used to store frame number
        frame = ""

    def get_image(self, frameNumber):
        
        
        frame = self.root.find(".//*[@name='{name}.png']".format(name = frameNumber))
        
        # grab an image out of a larger spritesheet
        image = pg.Surface((int(frame.attrib['w']), int(frame.attrib['h'])))
        
        image.blit(self.spritesheet, (0, 0), (int(frame.attrib['x']), int(frame.attrib['y']), int(frame.attrib['w']), int(frame.attrib['h'])))
        return image

class Player(pg.sprite.Sprite):
    ''' This class defines the sprite the player controls in the game.'''

    def __init__(self, game, x, y):
        '''This initializer takes the game scene as a paraemter, initalizes
        the image and rect attributes and other variables used for the player'''

        # Add itself to the general sprite group
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        
        # Set the sprite's image and sets the rect attributes
        self.game = game
        
        self.currentFrame = 1
        self.image = self.game.spriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        
        # Set the starting coordinates
        self.x = x
        self.y = y
        
        #states to check the player's status
        self.alive = True
        


    def move(self, dx=0, dy=0):
        '''This method will move the player on the x, y coordinate based on the
        input '''
        self.x += dx
        self.y += dy

    def update(self):
        '''Updates the player sprite '''
        
        self.currentFrame += 1
        
        self.image = self.game.spriteSheet.get_image(self.currentFrame)
        
        if self.currentFrame == 54:
            self.currentFrame = 1 
            
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE        

        