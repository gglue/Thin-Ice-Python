'''
Name: Victor Li
Date: 5/7/2020
Description: Pygame remake of Club Penguin's Thin-ice
'''

# Import classes used for the game
from data.classes.sprites import *

class Game():
    '''This class defines the main game'''

    def __init__(self):
        '''This initializer defines the caption and windows and starts up the game engine config'''
        
        # Starts up the game and the audio
        pg.init()
        pg.mixer.init()
        
        # Set title and icon
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        # Allows to hold down input keys
        pg.key.set_repeat(200, 175)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
    def loadData(self):
        '''This method loads data from files outside of Python'''
        self.playerSpriteSheet = Spritesheet(PLAYERSPRITE, PLAYERXML)
        self.waterSpriteSheet = Spritesheet(WATERSPRITE, WATERXML)
        self.keySpriteSheet = Spritesheet(KEYSPRITE, KEYXML)
        self.teleporterSpriteSheet = Spritesheet(TELEPORTERSPRITE, TELEPORTERXML)
        
        # Loads the Background music
        pg.mixer.music.load('data/sound/music.ogg')
        pg.mixer.music.set_volume(0.1)
        
        # Sound effect when a player moves
        self.moveSound = pg.mixer.Sound("data/sound/move.ogg")
        self.moveSound.set_volume(0.1)
        
        # Sound effect when a player finishs a level completely
        self.allTileComplete = pg.mixer.Sound("data/sound/allTileComplete.ogg")
        self.allTileComplete.set_volume(0.2)

        # Sound effect when a player dies
        self.deadSound = pg.mixer.Sound("data/sound/dead.ogg")
        self.deadSound.set_volume(0.2)

        # Sound effect when a player touches a treasure bag
        self.treasureSound = pg.mixer.Sound("data/sound/treasure.ogg")
        self.treasureSound.set_volume(0.2)

        # Sound effect when a player moves away from an ice tile
        self.iceBreakSound = pg.mixer.Sound("data/sound/breakIce.ogg")
        self.iceBreakSound.set_volume(0.2)
        
        # Sound effect when a player touches a key or unlocks a key socket
        self.keyGet = pg.mixer.Sound("data/sound/keyGet.ogg")
        self.keyGet.set_volume(0.2)

        # Sound effect when a player is resetted to the start
        self.resetSound = pg.mixer.Sound("data/sound/reset.ogg")
        self.resetSound.set_volume(0.2)
        
        # Sound effect when a player hits a moving block
        self.movingBlockSound = pg.mixer.Sound("data/sound/movingBlockSound.ogg")
        self.movingBlockSound.set_volume(0.2)
        
        # Sound effect when a player teleports
        self.teleportSound = pg.mixer.Sound("data/sound/teleportSound.ogg")
        self.teleportSound.set_volume(0.2)
        
    def loadMap(self):
        '''Load the current level by reading a parameter '''
        
        #Resets the map-related variables
        mapData = []
        totalFree = 0
        
        
        # Opens the file and appends all the data to mapData
        fileName = "data/maps/level%d.txt" % self.currentLevel
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
        self.scoreKeeperTop.totalTiles = (totalFree - (2 * 19))
        self.scoreKeeperTop.completeTiles = 0
        # update current level number
        self.scoreKeeperTop.currentLevel = self.currentLevel
        

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
        self.currentLevel = 18
        
        # Lets game remember last level you solved it
        self.lastLevelSolved = True
        
        # Checks if the moving block is moving
        self.blockIsMoving = False
        
        # Checks if the player can still teleport
        self.canTeleport = True            
        
        self.scoreKeeperTop = ScoreKeeperTop(self)
        self.scoreKeeperBottom = ScoreKeeperBottom(self)
        self.resetButton = Button(self, "reset", 65, HEIGHT - 13, 72, 21)
        
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
        self.scoreKeeperBottom.score = self.scoreKeeperBottom.previousScore
        
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
        
        if self.currentLevel == 20:
            # Play the score screen
            w = ScoreScreen(self.scoreKeeperTop, self.scoreKeeperBottom)
            w.new()
            w.run()
        
        # Empty out the map and load new map
        self.deleteMap()
        self.loadMap()
        
        # Reset key status
        self.hasKey = False
        
        # Reset teleporter status
        self.canTeleport = True
            
    def draw(self):
        '''This method draws all the sprites onto the screen '''
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
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.resetButton.rect.collidepoint(pg.mouse.get_pos()):
                    # Play reset animation and sounds and reset the map when hitting the button
                    self.reset()
                    self.player.setFrame(RESETTING)
                    self.playResetSounds()
                                
            if event.type == pg.KEYDOWN:
                # Exits the game with the ESC key                 
                # Arrow keys handle the moving
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.checkAndMove(dx=-1)
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.checkAndMove(dx=1)
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.checkAndMove(dy=-1)
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.checkAndMove(dy=1)
                        
               
        #If player moved, check if he's on the finish line
        if self.moved:
            # Update the scorekeepers
            self.scoreKeeperTop.completeTiles += 1
            self.scoreKeeperBottom.score += 1
            
            # Check if player touched the finish line yet
            if self.player.collideWithTile(self.endTile):
                
                
                # Checks if bonus score can be applied
                if self.scoreKeeperTop.checkFinish():
                    
                    
                    # Lets game remember last level you solved it
                    self.lastLevelSolved = True
                    
                    # Plays the bonus sound effect
                    self.allTileComplete.play()
                    
                    # Increase the number of solved by 1
                    self.scoreKeeperTop.solvedLevels += 1  
                    
                    # Gives x2 bonus score if no reset/death, otherwise give the normal score
                    
                    if not self.resetOnce:
                        self.scoreKeeperBottom.score += self.scoreKeeperTop.totalTiles * 2
                    else:
                        self.scoreKeeperBottom.score += self.scoreKeeperTop.totalTiles
                    
                                   
                
                # Remind game player didn't solve last level    
                else:
                    self.lastLevelSolved = False
                
                # Sets the previous score for the next level
                self.scoreKeeperBottom.previousScore = self.scoreKeeperBottom.score
                
                # Update the total number of tiles the player melted overall in the game so far
                self.scoreKeeperTop.playerMelted += self.scoreKeeperTop.completeTiles
                
                # Go to the next level
                self.nextLevel()
                
            
            # If treasure bag exists, check if player touched treasure bag, treasure only appears after level 3 in original game
            elif self.lastLevelSolved and self.currentLevel > TREASURELEVEL:
                if  self.player.collideWithTile(self.treasureTile):
                    self.treasureTile.kill()
                    self.treasureSound.play()
                    self.scoreKeeperBottom.score += 100
            
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
                        self.scoreKeeperTop.completeTiles -= 1
                        self.scoreKeeperBottom.score -= 1
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.secondTeleporter.x, self.secondTeleporter.y)
                            self.canTeleport = False

                            self.teleportSound.play()
                        
                    elif self.player.collideWithTile(self.secondTeleporter):
                        self.scoreKeeperTop.completeTiles -= 1
                        self.scoreKeeperBottom.score -= 1
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.firstTeleporter.x, self.firstTeleporter.y)
                            self.canTeleport = False

                            self.teleportSound.play()
                                                    
            # If the player collided with the moving block tile, don't add score
            if self.currentLevel > MOVINGBLOCKLEVEL and self.player.collideWithTile(self.movingBlockTile):
                self.scoreKeeperTop.completeTiles -= 1
                self.scoreKeeperBottom.score -= 1        
            
            # Checks if the player is unable to move anymore, continued
            # explaination in Player class
            if self.player.checkDeath():
                # Play death animation and sounds and reset the map when hitting the button
                self.player.setFrame(DYING)
                self.playResetSounds()            
                        
            # Reset moved variable
            self.moved = False
    
            
            
class TitleScreen():
    '''This class defines the title screen of the main game'''

    def __init__(self):
        '''This initializer takes the main menu scene as a parameter, initalizes
        the image and rect attributes and other variables used for the player'''
        
        # Starts up the game and the audio
        pg.init()
        pg.mixer.init()
        
        # Set title and icon
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

    def loadData(self):
        '''This method loads data from files outside of Python'''
        
        # Loads the Background music
        pg.mixer.music.load('data/sound/music.ogg')
        pg.mixer.music.set_volume(0.1)
        
        # Sound effect when you click the button
        self.clickSound = pg.mixer.Sound("data/sound/move.ogg")
        self.clickSound.set_volume(0.2)
         
    def new(self):
        '''This method initializes all the variables and sets up the game '''
        
        # Loads external data
        self.loadData()
        
        # Creates the groups used for event handling later on
        self.scoreSprites = pg.sprite.Group()
        
        # Plays and infinitely loops the music
        pg.mixer.music.play(-1)
        
        # Clock used to set the frame rate
        self.clock = pg.time.Clock()
        
        # Is the main menu pictures
        self.mainMenu = BeginMenu(self)
        
        # The starting picture
        self.startButton = Button(self, "start", 237, 390, 108, 32)

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
        self.scoreSprites.update()

    def events(self):
        '''This method handles the event handling'''
        
        # CONTROLS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.startButton.rect.collidepoint(pg.mouse.get_pos()) and self.startButton.buttonType == "start":
                    # When player clicks the start button, show the instruction screen
                    self.mainMenu.instructions()
                    self.startButton.__init__(self, "play", 237, 390, 108, 32)
                    self.clickSound.play()
                    
                elif event.button == 1 and self.startButton.rect.collidepoint(pg.mouse.get_pos()) and self.startButton.buttonType == "play":
                    self.clickSound.play()
                    # Start the actual game
                    x = Game()
                    x.new()
                    x.run()
                    
                    
    def draw(self):
        '''This method draws all the sprites onto the screen '''
        self.scoreSprites.draw(self.screen)
        pg.display.flip()

class ScoreScreen():
    ''' This class is the screen that displays your overall stats after finishing all 19 levels'''
    
    def __init__(self, scoreBoardTop, scoreBoardBottom):
        '''This initializer takes the main menu scene as a parameter, initalizes
        the image and rect attributes and other variables used for the player'''
        
        # Starts up the game and the audio
        pg.init()
        pg.mixer.init()
        
        # Set title and icon
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
        
        # The stats of the player
        self.levelSolved = scoreBoardTop.solvedLevels
        self.iceMelted = scoreBoardTop.playerMelted
        self.totalScore = scoreBoardBottom.score
          
    def loadData(self):
        '''This method loads data from files outside of Python'''
        
        # Loads the Background music
        pg.mixer.music.load('data/sound/winner.ogg')
        pg.mixer.music.set_volume(0.1)

        # Instantiate the font used for the game
        self.font = pg.font.Font("data/font/arcade.ttf", 18) 
        
        # Puffle image
        self.puffle= pg.image.load("data/images/puffle.png")
        
        # Sound effect when a line loads
        self.lineSound = pg.mixer.Sound("data/sound/move.ogg")
        self.lineSound.set_volume(0.2)
               
        # Sound effect when the puffle loads
        self.puffleSound = pg.mixer.Sound("data/sound/allTileComplete.ogg")
        self.puffleSound.set_volume(0.2)

    def new(self):
        '''This method initializes all the variables and sets up the game '''
        
        # Loads external data
        self.loadData()
        
        # Creates the groups used for event handling later on
        self.scoreSprites = pg.sprite.Group()
        
        # Plays and infinitely loops the music
        pg.mixer.music.play(-1)
        
        # Clock used to set the frame rate
        self.clock = pg.time.Clock()
        
        # Counter used to display text in a timely manner
        self.counter = 0
                
        # The button to close the game
        self.finishButton = Button(self, "finish", 237, 390, 108, 32)
        
        self.levelSolvedText = self.font.render("Total levels solved:%21d" % self.levelSolved, 1 , (0,0,0))
        self.iceMeltedText = self.font.render("Total ice melted:%25d" % self.iceMelted, 1 , (0,0,0))
        self.totalScoreText = self.font.render("Total points:%32d" % self.totalScore, 1, (0,0,0))
        
        # Light blue background
        self.screen.fill((217,241, 255))
               
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
        self.scoreSprites.update()
        
        # Blits each stat line every 0.75 seconds
        if self.counter == 1:
            self.screen.blit(self.levelSolvedText, (75,25))
            pg.time.delay(750)
            self.lineSound.play()
        elif self.counter == 2:
            self.screen.blit(self.iceMeltedText, (75,75))
            pg.time.delay(750)
            self.lineSound.play()
        elif self.counter == 3:
            self.screen.blit(self.totalScoreText, (75,125))
            pg.time.delay(750)
            self.lineSound.play()
        elif self.counter == 4:
            self.screen.blit(self.puffle, (170,150))
            pg.time.delay(750)
            self.puffleSound.play()
        self.counter += 1 
        
    def events(self):
        '''This method handles the event handling'''
        
        # CONTROLS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.finishButton.rect.collidepoint(pg.mouse.get_pos()) and self.finishButton.buttonType == "finish":
                    pg.quit()
                    exit()
                    
                    
    def draw(self):
        '''This method draws all the sprites onto the screen '''
        self.scoreSprites.draw(self.screen)       
        pg.display.flip()
        
g = TitleScreen()

while True:
    g.new()
    g.run()
