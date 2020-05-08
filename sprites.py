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
    
    def __init__(self, filename, xmlName):
        '''This initializer takes the file name as a parameter to load'''
        
        #Loads the PNG file
        self.spritesheet = pg.image.load(filename).convert()
        
        #Loads the XML file
        self.xml = ET.parse(xmlName)
        self.root = self.xml.getroot() 
        
        #Variable used to store frame number
        frame = ""

    def get_image(self, frameNumber):
        
        
        frame = self.root.find(".//*[@name='%s.png']"% frameNumber)
        
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
        self.image = self.game.playerSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()
        
        # Set the starting coordinates
        self.x = x
        self.y = y
        
        #states to check the player's status
        # 1 = alive
        # 2 = dead
        # 3 = respawning
        self.status = 1
        


    def move(self, dx=0, dy=0):
        '''This method will move the player on the x, y coordinate based on the
        input '''
        if not self.collide_with_walls(dx, dy):
            
            # Create a water tile at the previous position
            Water(self.game, self.x, self.y)
            
            # Update position
            self.x += dx
            self.y += dy
            
            # Update the scorekeeper
            self.game.scoreKeeperTop.setCompleteTiles(self.game.scoreKeeperTop.getCompleteTiles() + 1)            
            
            # Play the sound
            self.game.moveSound.play()

    def update(self):
        '''This method updates the player sprite '''
        
        self.currentFrame += 1
        
        self.image = self.game.playerSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        if self.currentFrame == 54:
            self.currentFrame = 1 
        
        # Updates the position
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def collide_with_walls(self, dx=0, dy=0):
        ''' This method checks if the player has collison with any walls '''
        
        # Checks all the wall entities
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
               
        # Allow player to move if theres nothing blocking
        return False

        

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
        
        
class Wall(Immovable):
    ''' This class represents a wall in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("images/wall.png")
                          
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
        
        self.image = pg.image.load("images/free.png")
        self.image.set_colorkey((255,255,255))
        
class End(Movable):
    ''' This class represents the finish line in game '''
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("images/finish.png")
        self.image.set_colorkey((255,255,255))
        
        
class Unused(pg.sprite.Sprite):
    ''' This class represents an unused tile in game '''
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("images/unused.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.image.set_colorkey((0,0,0))
        
class ScoreKeeperTop(pg.sprite.Sprite):
    ''' This class defines the scoreboard in where you keep track of the current score '''
    
    def __init__(self, game):
        ''' Initalizer takes the screen surface parameters to set location of the scorekeeper '''
        
        #Adds to all sprite group
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Call the sprite __init__() method
        pg.sprite.Sprite.__init__(self)

        # Sets the font used for the sprite
        self.font = pg.font.Font('font/arcade.ttf', 16)
        
        # Set instance variables used to track score
        self.currentLevel = 1
        self.completeTiles = 0
        self.totalTiles = 0
        self.solvedLevels = 0

        # The text that contains the score that constantly update
        self.message = ""
        self.image = self.font.render(self.message, 1, (0, 0, 0))
        
        # Set the position of the sprites
        
        self.rect = self.image.get_rect()
        self.rect.centery = TILESIZE - 15
        
        self.message = " "
        
        # Variable just used for keeping track of the game
        self.game = game
        
    def setTotalTiles(self, amount):
        ''' This method lets the scoreboard know the total number of free tiles '''
        self.totalTiles = amount
        
    def getTotalTiles(self):
        ''' This method returns the total number of free tiles '''
        return self.totalTiles      
        
    def setCompleteTiles(self, amount):
        ''' This method lets the scoreboard know the total number of complete tiles '''
        self.completeTiles = amount
        
    def getCompleteTiles(self):
        ''' This method returns the total number of complete tiles '''
        return self.completeTiles            
        
        
    def setCurrentLevel(self, amount):
        ''' This method lets the scoreboard know the current level'''
        self.currentLevel = amount
        
    def setSolvedLevels(self, amount):
        ''' This method lets the scoreboard know the number of solved levels'''
        self.solvedLevels = amount
    
    def update(self):
        '''This method will be called automatically to display 
        the game information at the top of the game window.'''
 
        # The text that contains the score that constantly update
        self.message = "%11s%3d%20d%s%-20d%s%3d" % ( "LEVEL", self.currentLevel, self.completeTiles,\
                                                                               "/", self.totalTiles, "SOLVED", self.solvedLevels)
        self.image = self.font.render(self.message, 1, (0, 0, 0))
               