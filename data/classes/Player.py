import pygame as pg
from data.classes.settings import *
from data.classes.Immovable import Water
from data.classes.Movable import Free
class Player(pg.sprite.Sprite):
    ''' This class defines the sprite the player controls in the game.'''

    def __init__(self, game, x, y):
        '''This initializer takes the game scene as a paraemter, initalizes
        the image and rect attributes and other variables used for the player'''

        # Add itself to the general sprite group
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        
        # Set the sprite's image and sets the rect attributes
        self.game = game
        
        self.currentFrame = 16
        self.image = self.game.playerSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()
        
        # Set the starting coordinates
        self.x = x
        self.y = y
        
        
    def movetoCoordinate(self, x, y):
        ''' This method moves the player to a specific coordinate '''
        self.x = x
        self.y = y
         
    def setFrame(self, frameNumber):
        ''' This method sets the current frame of animation '''
        self.currentFrame = frameNumber
        
    def getFrame(self):
        ''' This method gets the current frame of animation '''
        return self.currentFrame
    
    def move(self, dx=0, dy=0):
        '''This method will move the player on the x, y coordinate based on the
        input '''
            
        # Update position
        self.x += dx
        self.y += dy
                        
        # Play the sound
        self.game.moveSound.play()
        
        # Lets the game know the player successfully moved
        self.game.moved = True
            
    def checkAndMove(self, dx=0, dy=0):
        ''' This method combines multiple other methods for better readability in the main program '''
                
        # Only start checking when the moving block is active, move the moving block when the player moves towards it
        if self.game.currentLevel > MOVINGBLOCKLEVEL and self.nearTile(self.game.movingBlock) != 0:
            locationOfPlayer = self.nearTile(self.game.movingBlock)
            self.game.blockIsMoving = True
            
            if locationOfPlayer == 1 and dx == -1 and dy == 0:
                self.game.movingBlock.setVelocity(dx,dy)
            elif locationOfPlayer == 2 and dx == 1 and dy == 0:
                self.game.movingBlock.setVelocity(dx,dy)
            elif locationOfPlayer == 3 and dx == 0 and dy == -1:
                self.game.movingBlock.setVelocity(dx,dy)
            elif locationOfPlayer == 4 and dx == 0 and dy == 1:
                self.game.movingBlock.setVelocity(dx,dy)
            
            
            # If the player is not near a moving block, just do the normal collison check                        
            else:
                if not self.collideWithGroup(self.game.walls, dx, dy):
                    if self.checkMakeWater() and not self.collideWithGroup(self.game.noWaterGroup, 0, 0):
                        Water(self.game, self.x, self.y)
                    self.move(dx,dy)                    
        
        
        # When it's the earlier levels, just check if the player is colliding with a wall
        elif not self.collideWithGroup(self.game.walls, dx, dy):
            if self.checkMakeWater() and not self.collideWithGroup(self.game.noWaterGroup, 0, 0):
                Water(self.game, self.x, self.y)
            self.move(dx,dy)
                         
    def update(self):
        '''This method updates the player sprite '''
        
        self.currentFrame += 1
        
        self.image = self.game.playerSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        
        # I would implement switch case but it doesn't exist in Python
        # Changes the animation of the sprite based on status variable
        
        # THIS IS OUT OF PLACE BUT THE ONLY EFFICIENT WAY TO DO IT
        # When finishing death animation, resets the map
        if self.currentFrame == 15:
            self.game.reset()
        
        if self.currentFrame == 86:
            self.currentFrame = 28 
        
        # Updates the position
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    
    
    def checkMakeWater(self):
        ''' This method checks if the game should make a water tile in the player's previous position '''
        
        for ice in self.game.iceSprites:
            # If player was on an ice block, kill it, spawn a Free tile on it instead and play the sound effect
            if ice.x == self.x and ice.y == self.y:
                ice.kill()
                Free(self.game, self.x, self.y)
                self.game.iceBreakSound.play()
                return False
            
        # Return True if not on an ice block
        return True
    
        
    def collideWithGroup(self, nameOfGroup, dx=0, dy=0):
        ''' This method checks if the player has collison with a group's entities '''
 
        # Checks all the group's entities
        for entity in nameOfGroup:
            if entity.x == self.x + dx and entity.y == self.y + dy:
                return True
               
        # Allow player to move if theres nothing blocking
        return False
    
    def collideWithTile(self, tile):
        ''' This method checks if the player is in the same tile as the parameter '''
        
        # True if on the same tile
        if tile.x == self.x and tile.y == self.y:
            return True
        else:
            return False

    def nearTile(self, tile):
        ''' This method checks if the player is near the same tile as the parameter '''
        
        # 0 = not near
        # 1 = left
        # 2 = right
        # 3 = up
        # 4 = down
        if tile.x == self.x - 1 and tile.y == self.y + 0:
            return 1
        elif tile.x == self.x + 1 and tile.y == self.y + 0:
            return 2
        elif tile.x == self.x + 0 and tile.y == self.y - 1:
            return 3
        elif tile.x == self.x + 0 and tile.y == self.y + 1:
            return 4
        
        return 0
    
        
    def checkDeath(self):
        ''' This method checks if the player is stuck '''
        
        left = False
        right = False
        top = False
        bottom = False
        
       
        
        # Checks if the player is able to walk anymore, true meaning can't got that direction
        for wall in self.game.walls:
            if wall.x == self.x - 1 and wall.y == self.y + 0:
                left = True
            elif wall.x == self.x + 1 and wall.y == self.y + 0:
                right = True
            elif wall.x == self.x + 0 and wall.y == self.y - 1:
                top = True
            elif wall.x == self.x + 0 and wall.y == self.y + 1:
                bottom = True             
        
        # If all true, it means the player can't move and must die/reset and returns True
        if left and right and top and bottom:
            Water(self.game, self.x, self.y)
            return True
        else:
            return False
            
