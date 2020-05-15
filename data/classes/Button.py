import pygame as pg

class Button(pg.sprite.Sprite):
    ''' This class represents a clickable button in the game '''
    
    def __init__(self, game, buttonType, xCoordinate, yCoordinate, width, height):
        '''This initializer takes the game scene as a paraemter, initalizes
        the image and rect attributes and other variables used for the player'''
        
        
        # Game variable for references
        self.game = game
        
        # Add itself to the score sprite group
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Different button type means different images
        if buttonType == "reset":
            self.buttonImages = ["data/images/resetButtonOne.png", "data/images/resetButtonTwo.png"]
            
        elif buttonType == "start":
            self.buttonImages = ["data/images/startButtonOne.png", "data/images/startButtonTwo.png"]
            
        elif buttonType == "play":
            self.buttonImages = ["data/images/playButtonOne.png", "data/images/playButtonTwo.png"]
            
        else:
            self.buttonImages = ["data/images/finishButtonOne.png", "data/images/finishButtonTwo.png"]
        # Set the width and height of the button
        self.width = width
        self.height = height
        
        # Stores what type of button it is
        self.buttonType = buttonType
        
        # Set the image
        self.image = pg.image.load(self.buttonImages[0])
        
        # Resize the button
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        
        
        # Set the location of the button
        self.rect = self.image.get_rect()
        self.rect.centery = yCoordinate
        self.rect.centerx = xCoordinate
        self.image.set_colorkey((255,255,255))
        
    def getRect(self):
        '''Returns the rect properities of the button '''
        return self.rect
    
    def setImage(self, number):
        '''Sets the image using the image array based on the parameter '''
        
        # Set the image
        self.image = pg.image.load(self.buttonImages[number])
        
        # Resize the button
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        
    def update(self):
        '''Updates the game sprite based on my mouse input '''
        
        # Check if mouse is hovering over reset button
        if self.getRect().collidepoint(pg.mouse.get_pos()):
            self.setImage(1)
        else:
            self.setImage(0)
