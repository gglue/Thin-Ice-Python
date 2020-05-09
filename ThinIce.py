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
        
        # Starts up the game and the audio
        pg.init()
        pg.mixer.init()
        
        # Set title and icon
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('images/icon.png'))
        
        # Allows to hold down input keys
        pg.key.set_repeat(150, 150)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
        # Clock used to set the frame rate
        self.clock = pg.time.Clock()
        
        # Contains the end point of each level for event handling
        self.endTile = object()
        
        # Checks if player has reset once on the map
        self.resetOnce = False
        
        # Checks if the player has moved successfully
        self.moved = False
              
    def loadData(self):
        '''This method loads data from files outside of Python'''
        self.playerSpriteSheet = Spritesheet(PLAYERSPRITE, PLAYERXML)
        self.waterSpriteSheet = Spritesheet(WATERSPRITE, WATERXML)
        
        # Loads the Background music
        pg.mixer.music.load('sound/music.mp3')
        pg.mixer.music.set_volume(0.1)
        
        # Sound effect when a player moves
        self.moveSound = pg.mixer.Sound("sound/move.mp3")
        self.moveSound.set_volume(0.05)
        
        # Sound effect when a player finishs a level completely
        self.allTileComplete = pg.mixer.Sound("sound/allTileComplete.mp3")
        self.allTileComplete.set_volume(0.05)
        
    def loadMap(self):
        '''Load the current level by reading a .txt '''
        
        #Resets the map-related variables
        mapData = []
        totalFree = 1
        # Opens the file and appends all the data to mapData
        currentMap = open("maps/levelOne.txt", "r")
        for line in currentMap:
            mapData.append(line)
        
        
        # Generates the map based on the text file    
        for row, tiles in enumerate(mapData):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == '0':
                    Unused(self, col, row)
                if tile == 'F':
                    Free(self, col, row)
                    totalFree += 1
                if tile == 'E':
                    self.endTile = End(self, col, row)
                if tile == 'P':
                    Free(self, col, row)
                    self.player.movetoCoordinate(col,row)
        
        # subtracting the top row and bottom row free because they're meant for the menu lol            
        self.scoreKeeperTop.setTotalTiles(totalFree - (2*19))
                    


    def new(self):
        '''This method initializes all the variables and sets up the game '''
        
        # Loads external data
        self.loadData()
        
        # Creates the groups used for event handling later on
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.movable = pg.sprite.Group()
        self.scoreSprites = pg.sprite.Group()
        
        # Currents the player sprite before the map loading
        self.player = Player(self, 0, 0)        
        
        self.scoreKeeperTop = ScoreKeeperTop(self)
        self.scoreKeeperBottom = ScoreKeeperBottom(self)
        self.resetButton = Button(self, "reset", 65, HEIGHT - 13)
        
        # Load the map
        self.loadMap()
        
        # Plays and infinitely loops the music
        pg.mixer.music.play(-1)
        

    def run(self):
        '''This method is the game loop which runs most of the game '''
        self.looping = True
        while self.looping:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            

    def update(self):
        '''This method updates all classes/objects as part of the game loop '''
        self.allSprites.update()
        self.scoreSprites.update()


    def drawGrid(self):
        '''This method draws the grid for more precise x,y coordinates '''
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def reset(self):
        ''' This method resets the current level '''
        print("reset")
        
        # Empty out the map and reload the map
        self.walls.empty()
        self.movable.empty()
        self.loadMap()
        
        # Reset the score to 0 or to previous level
        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getPreviousScore())
        self.scoreKeeperTop.setCompleteTiles(0)
        
        # Tells the game the player reset once
        self.resetOnce = True
            
    def draw(self):
        '''This method draws all the sprites onto the screen '''
        self.screen.fill(BGCOLOR)
        #self.drawGrid()
        self.allSprites.draw(self.screen)
        self.scoreSprites.draw(self.screen)
        pg.display.flip()
              

    def events(self):
        '''This method handles the event handling'''
        
        # CONTROLS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.resetButton.rect.collidepoint(pg.mouse.get_pos()):
                    self.reset()
                
                
            if event.type == pg.KEYDOWN:
                # Exits the game with the ESC key
                if event.key == pg.K_ESCAPE:
                    self.quit()
                    
                # Arrow keys handle the moving
                if event.key == pg.K_LEFT:
                    if not self.player.collideWithWalls(dx=-1):
                        self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    if not self.player.collideWithWalls(dx=1):
                        self.player.move(dx=1)
                if event.key == pg.K_UP:
                    if not self.player.collideWithWalls(dy=-1):
                        self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    if not self.player.collideWithWalls(dy=1):
                        self.player.move(dy=1)
                        
               
        #If player moved, check if he's on the finish line
        if self.moved:
            
            # Update the scorekeepers
            self.scoreKeeperTop.setCompleteTiles(self.scoreKeeperTop.getCompleteTiles() + 1)
            self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + 1)            
            
            if self.player.collideWithFinish():
                print("you win")
                self.allTileComplete.play()
                
                #Checks if bonus score can be applied
                if self.scoreKeeperTop.checkFinish():
                    # Gives x2 bonus score if no reset/death, otherwise give the normal score
                    
                    if not self.resetOnce:
                        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + self.scoreKeeperTop.getTotalTiles() * 2)
                        self.scoreKeeperBottom.setPreviousScore(self.scoreKeeperBottom.getScore())
                        
                    else:
                        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + self.scoreKeeperTop.getTotalTiles())
                        self.scoreKeeperBottom.setPreviousScore(self.scoreKeeperBottom.getScore())
                               
                    #game.nextLevel()
            else:
                print("moving")
                
            self.moved = False
            
        

g = Game()
while True:
    g.new()
    g.run()
