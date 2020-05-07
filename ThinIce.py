'''
Name: Victor Li
Date: 5/7/2020
Description: Pygame remake of Club Penguin's Thin-ice
'''

# Import classes used for the game
import pygame as pg
from sprites import *
from settings import *


class Game():
    '''This class defines the main game'''

    def __init__(self):
        '''This initalizer takes the game scene as a paraemter, initalizes
        the image and rect attributes and other variables used for the player'''
        pg.init()
        pg.display.set_caption("Thin-Ice!")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))


    def new(self):
        '''This method initializes all the variables and sets up the game '''
        self.allSprites = pg.sprite.Group()
        self.player = Player(self, 10, 10)

    def run(self):
        '''This method is the game loop which runs most of the game '''
        self.looping = True
        while self.looping:
            self.events()
            self.update()
            self.draw()

    def update(self):
        '''Updates all classes/objects as part of the game loop '''
        self.allSprites.update()

    def drawGrid(self):
        '''Draws the grid for more precise x,y coordinates '''
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        self.allSprites.draw(self.screen)
        pg.display.flip()            

    def events(self):
        '''Event handling'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

g = Game()
while True:
    g.new()
    g.run()
