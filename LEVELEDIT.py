#LEVEL EDITOR - ESCAPE GLADOS
from pygame import *
import os
import pickle
from pprint import *


def drawAll(screen,output,image):
    screen.blit(image,(0,0))
    for x in range(80):
        for y in range(60):
            c = level[x][y]
            if c != 0:
                draw.rect(screen,col[c], (x*10,y*10,10,10))
                
def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")
        return pickle.load(myPFile)       
    else:
        return [[0]*60 for x in range(80)]
    
def saveMap(level, fname):
    myPFile = open("level1.p", "wb")
    pickle.dump(level, myPFile)

screen = display.set_mode((800,600))
col = [(0,0,0),(0,255,0),(255,255,255),(255,0,0),(0,0,255),(0,255,255),(0,0,0),(0,0,0)]#nothing,can portal,cant portal,jump pad, launch pad left, launch pad right 
current = 1
back = image.load("background.bmp")
level = loadMap("level1.p")
running = True

while running:
    for e in event.get():                
        if e.type == QUIT:
            running = False
            
    keys = key.get_pressed()                
    for i in range(8):
        if keys[i+48]:
            current = i
        
    if mouse.get_pressed()[0]:
        mx, my = mouse.get_pos()
        gx = mx // 10
        gy = my // 10
        level[gx][gy] = current
        draw.rect(screen, col[level[gx][gy]], (gx*10, gy*10, 10, 10))
        
    if mouse.get_pressed()[2]:
        mx, my = mouse.get_pos()
        gx = mx // 10
        gy = my // 10
        level[gx][gy] = 0
        
    drawAll(screen, level, back)
    display.flip()

    
quit()
saveMap(level, "level1.p")
