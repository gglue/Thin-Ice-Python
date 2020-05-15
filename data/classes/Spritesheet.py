import pygame as pg
import xml.etree.ElementTree as ET
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