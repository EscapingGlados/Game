#LEVEL EDITOR
from pygame import *
import os
import pickle
from math import *
import time
import glob

def Main():
    backg = image.load("checking_level1.png")
    screen = display.set_mode((800,600))
    showing = True
    typing = False
    loadingScreen = False
    font.init()


    def drawAll(screen,output,image):
        screen.blit(image,(0,0))
        for x in range(80):
            for y in range(60):
                c = output[x][y]
                if c != 0:
                    draw.rect(screen,col[c], (x*10,y*10,10,10))
                    
    def loadMap(fname):
        if fname in os.listdir("."):
            myPFile = open(fname, "rb")
            return pickle.load(myPFile)       
        else:
            return [[0]*60 for x in range(80)]


    upheav = font.Font("upheavtt.ttf",40)
    name = ""
    running = True

    def text(msg,x,y):
        words = upheav.render(msg, True,(0,255,255))
        screen.blit(words,(x,y))
    while running:
        click = False
        for e in event.get():                
            if e.type == QUIT:
                operation = 'exit'
                running = False

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
      
                        
        mx, my = mouse.get_pos()


        picList = glob.glob("*_map")
            

        screen.blit(backg,(0,0))
                    
        for i in range(len(picList)):
            if Rect(200,50*i+200,600,50).collidepoint((mx,my)):
                if click:
                    levelName = picList[i]
                    operation = 'edit'
                    running = False
                    
                    
                    time.sleep(0.05)
                draw.rect(screen,(255,0,0),(200,50*i+200,400,50))
                
            text(picList[i][:-4],200,50*i+200)
                           
        display.flip()
    print(levelName)
    return operation,levelName
