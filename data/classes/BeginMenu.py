import pygame as pg
class BeginMenu(pg.sprite.Sprite):
    '''This class represents the images used for the start menu '''
    
    def __init__(self, game):
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.menuImages = ['data/images/titleScreen.png', 'data/images/instructionScreen.png']
        
        self.image = pg.image.load(self.menuImages[0])
        
        self.rect = self.image.get_rect()
        
        
    def instructions(self):
        ''' This function changes the main menu picture to the second '''
        self.image = pg.image.load(self.menuImages[1])
        self.rect = self.image.get_rect()