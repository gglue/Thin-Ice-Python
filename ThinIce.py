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
        
        # Tells where to move the moving block later
        self.movingBlockTile = object()
        
        # Checks if player can open a key socket
        self.hasKey = False

        # Checks if player has reset once on the map
        self.resetOnce = False
        
        # Checks if the player has moved successfully
        self.moved = False
        
        # Contains the current level of the game
        self.currentLevel = 1
        
        # Lets game remember last level you solved it
        self.lastLevelSolved = True
        
        # Checks if the moving block is moving
        self.blockIsMoving = False
        
        # Checks if the player can still teleport
        self.canTeleport = True
              
    def loadData(self):
        '''This method loads data from files outside of Python'''
        self.playerSpriteSheet = Spritesheet(PLAYERSPRITE, PLAYERXML)
        self.waterSpriteSheet = Spritesheet(WATERSPRITE, WATERXML)
        self.keySpriteSheet = Spritesheet(KEYSPRITE, KEYXML)
        self.teleporterSpriteSheet = Spritesheet(TELEPORTERSPRITE, TELEPORTERXML)
        
        # Loads the Background music
        pg.mixer.music.load('sound/music.mp3')
        pg.mixer.music.set_volume(0.1)
        
        # Sound effect when a player moves
        self.moveSound = pg.mixer.Sound("sound/move.wav")
        self.moveSound.set_volume(0.05)
        
        # Sound effect when a player finishs a level completely
        self.allTileComplete = pg.mixer.Sound("sound/allTileComplete.wav")
        self.allTileComplete.set_volume(0.05)

        # Sound effect when a player dies
        self.deadSound = pg.mixer.Sound("sound/dead.wav")
        self.deadSound.set_volume(0.1)

        # Sound effect when a player touches a treasure bag
        self.treasureSound = pg.mixer.Sound("sound/treasure.wav")
        self.treasureSound.set_volume(0.1)

        # Sound effect when a player moves away from an ice tile
        self.iceBreakSound = pg.mixer.Sound("sound/breakIce.wav")
        self.iceBreakSound.set_volume(0.1)
        
        # Sound effect when a player touches a key or unlocks a key socket
        self.keyGet = pg.mixer.Sound("sound/keyGet.wav")
        self.keyGet.set_volume(0.1)

        # Sound effect when a player is resetted to the start
        self.resetSound = pg.mixer.Sound("sound/reset.wav")
        self.resetSound.set_volume(0.1)
        
        # Sound effect when a player hits a moving block
        self.movingBlockSound = pg.mixer.Sound("sound/movingBlockSound.wav")
        self.movingBlockSound.set_volume(0.1)
        
        # Sound effect when a player teleports
        self.teleportSound = pg.mixer.Sound("sound/teleportSound.wav")
        self.teleportSound.set_volume(0.1)
        
    def loadMap(self):
        '''Load the current level by reading a parameter '''
        
        #Resets the map-related variables
        mapData = []
        totalFree = 0
        
        
        # Opens the file and appends all the data to mapData
        fileName = "maps/level%d.txt" % self.currentLevel
        currentMap = open(fileName, "r")
        for line in currentMap:
            mapData.append(line)
        
        
        # Generates the map based on the text file    
        for row, tiles in enumerate(mapData):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                elif tile == '0':
                    Unused(self, col, row)
                elif tile == 'F':
                    Free(self, col, row)
                    totalFree += 1
                elif tile == 'E':
                    self.endTile = End(self, col, row)
                elif tile == 'I':
                    Ice(self, col, row)
                    totalFree +=2
                elif tile == 'K':
                    Free(self, col, row)
                    self.key = GoldenKey(self, col, row)
                    totalFree +=1
                elif tile == 'B':
                    self.movingBlockTile = MovingBlockTile(self, col, row)
                elif tile == 'T':
                    Free(self, col, row)
                    self.movingBlock = MovingBlock(self, col, row)     
                    totalFree += 1
                elif tile == '%':
                    # exclusive tile only used for level 14,15,16
                    Ice(self, col, row)
                    self.movingBlock = MovingBlock(self,col,row)
                    totalFree += 2
                elif tile == '&':
                    # exclusive tile only used for level 15
                    self.movingBlockTile = MovingBlockTile(self, col, row)
                    self.key = GoldenKey(self, col, row)
                elif tile == '!':
                    # exclusive tile only used for level 16
                    Ice(self, col, row)
                    self.key = GoldenKey(self, col, row)
                    totalFree += 2
                elif tile == '1':
                    # teleporter 1
                    self.firstTeleporter = Teleporter(self, col, row)
                elif tile == '2':
                    # teleporter 2
                    self.secondTeleporter = Teleporter(self, col, row)
                elif tile == 'H':
                    self.keyHole = KeyHole(self, col, row)
                    totalFree += 1
                elif tile == 'M':
                    Free(self, col, row)
                    if (self.lastLevelSolved):
                        self.treasureTile = Treasure(self, col, row)
                    totalFree += 1
                elif tile == 'P':
                    Free(self, col, row)
                    self.player.movetoCoordinate(col,row)
                    totalFree += 1
        
        # subtracting the top row and bottom row free because they're meant for the menu lol            
        self.scoreKeeperTop.setTotalTiles(totalFree - (2*19))
        self.scoreKeeperTop.setCompleteTiles(0)
        # update current level number
        self.scoreKeeperTop.setCurrentLevel(self.currentLevel)
        

    def new(self):
        '''This method initializes all the variables and sets up the game '''
        
        # Loads external data
        self.loadData()
        
        # Creates the groups used for event handling later on
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.movable = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.iceSprites = pg.sprite.Group()
        self.scoreSprites = pg.sprite.Group()
        self.updatingBlockGroup = pg.sprite.Group()
        self.noWaterGroup = pg.sprite.Group()
        
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
    
    def deleteMap(self):
        '''This method deletes all tiles in the current level '''
        for tiles in self.allSprites:
            tiles.kill()
            
    def playResetSounds(self):
        '''This method plays the relevant sounds when you reset or when you die '''
        self.deadSound.play()
        self.resetSound.play()        
    
               
    def reset(self):
        ''' This method resets the current level '''
        
        # Empty out the map and reload the map
        self.deleteMap()
        self.loadMap()
        
        # Reset the score to 0 or to previous level
        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getPreviousScore())
        
        # Reset key status
        self.hasKey = False
        
        # Reset teleporter status
        self.canTeleport = True
        
        # Tells the game the player reset once
        self.resetOnce = True
        
    
    def nextLevel(self):
        ''' This method moves the player to the next level '''
        
        #Updates variables
        self.resetOnce = False
        self.currentLevel += 1
        
        # Empty out the map and load new map
        self.deleteMap()
        self.loadMap()        
            
    def draw(self):
        '''This method draws all the sprites onto the screen '''
        self.screen.fill(BGCOLOR)
        #self.drawGrid()
        self.allSprites.draw(self.screen)
        self.scoreSprites.draw(self.screen)
        self.updatingBlockGroup.draw(self.screen)
        pg.display.flip()
              

    def events(self):
        '''This method handles the event handling'''
        
        # CONTROLS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.resetButton.rect.collidepoint(pg.mouse.get_pos()):
                    # Play reset animation and sounds and reset the map when hitting the button
                    self.reset()
                    self.player.setFrame(RESETTING)
                    self.playResetSounds()
                
                
            if event.type == pg.KEYDOWN:
                # Exits the game with the ESC key
                if event.key == pg.K_ESCAPE:
                    self.quit()
                    
                # Arrow keys handle the moving
                if event.key == pg.K_LEFT:
                    self.player.checkAndMove(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.checkAndMove(dx=1)
                if event.key == pg.K_UP:
                    self.player.checkAndMove(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.checkAndMove(dy=1)
                        
               
        #If player moved, check if he's on the finish line
        if self.moved:
            print(len(self.allSprites))
            # Update the scorekeepers
            self.scoreKeeperTop.setCompleteTiles(self.scoreKeeperTop.getCompleteTiles() + 1)
            self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + 1)
            
            # Check if player touched the finish line yet
            if self.player.collideWithTile(self.endTile):
                
                
                # Checks if bonus score can be applied
                if self.scoreKeeperTop.checkFinish():
                    
                    
                    # Lets game remember last level you solved it
                    self.lastLevelSolved = True
                    
                    # Plays the bonus sound effect
                    self.allTileComplete.play()
                    
                    # Increase the number of solved by 1
                    self.scoreKeeperTop.setSolvedLevel(self.scoreKeeperTop.getSolvedLevel() + 1)  
                    
                    # Gives x2 bonus score if no reset/death, otherwise give the normal score
                    
                    if not self.resetOnce:
                        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + self.scoreKeeperTop.getTotalTiles() * 2)
                        self.scoreKeeperBottom.setPreviousScore(self.scoreKeeperBottom.getScore())
                        
                    else:
                        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + self.scoreKeeperTop.getTotalTiles())
                        self.scoreKeeperBottom.setPreviousScore(self.scoreKeeperBottom.getScore())
                    
                
                # Remind game player didn't solve last level    
                else:
                    self.lastLevelSolved = False
                
                # Go to the next level
                self.nextLevel()
                
            
            # If treasure bag exists, check if player touched treasure bag, treasure only appears after level 3 in original game
            elif self.lastLevelSolved and self.currentLevel > TREASURELEVEL and self.currentLevel != 19:
                if  self.player.collideWithTile(self.treasureTile):
                    self.treasureTile.kill()
                    self.treasureSound.play()
                    self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() + 100)
            
            # Check if player touches key, only appears after level 9 in the original game        
            if self.currentLevel > KEYLEVEL:
                if self.player.collideWithTile(self.key):
                    # Lets player open key sockets now
                    self.key.kill()
                    self.keyGet.play()
                    self.hasKey = True
            
            
            # If the player currently has the key, check if he's in the radius of the keyhole
            if self.hasKey:
                if self.player.nearTile(self.keyHole) != 0:
                    #Delete the keyhole and replace with a free tile
                    Free(self, self.keyHole.x, self.keyHole.y)
                    self.keyGet.play()
                    self.keyHole.kill()
                    self.hasKey = False
                    
            # Checks if the player is able to teleport, only after level 16
            if self.currentLevel > TELEPORTLEVEL:
                    # Teleports to you to the other teleporter, make sure not to add score as well
                    if self.player.collideWithTile(self.firstTeleporter):
                        self.scoreKeeperTop.setCompleteTiles(self.scoreKeeperTop.getCompleteTiles() - 1)
                        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() - 1) 
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.secondTeleporter.x, self.secondTeleporter.y)
                            self.canTeleport = False

                            self.teleportSound.play()
                        
                    elif self.player.collideWithTile(self.secondTeleporter):
                        self.scoreKeeperTop.setCompleteTiles(self.scoreKeeperTop.getCompleteTiles() - 1)
                        self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() - 1)
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.firstTeleporter.x, self.firstTeleporter.y)
                            self.canTeleport = False

                            self.teleportSound.play()
                            
                
                        
                        
            # If the player collided with the moving block tile, don't add score
            if self.currentLevel > MOVINGBLOCKLEVEL and self.player.collideWithTile(self.movingBlockTile):
                self.scoreKeeperTop.setCompleteTiles(self.scoreKeeperTop.getCompleteTiles() - 1)
                self.scoreKeeperBottom.setScore(self.scoreKeeperBottom.getScore() - 1)                
            
            # Checks if the player is unable to move anymore, continued
            # explaination in Player class
            if self.player.checkDeath():
                # Play death animation and sounds and reset the map when hitting the button
                self.player.setFrame(DYING)
                self.playResetSounds()            
                        
            # Reset moved variable
            self.moved = False
    
            
            

g = Game()
while True:
    g.new()
    g.run()
