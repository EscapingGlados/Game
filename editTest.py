#LEVEL EDITOR
from pygame import *
import os
import pickle
from math import *
import time
import glob

showing = True
typing = False
loadingScreen = False
font.init()
rekt = Rect(750,550,50,50)
loadRect = Rect(700,550,50,50)

left = image.load("launch_left_block.png")
right = image.load("launch_right_block.png")
up = image.load("jump_block.png")



iconleft = transform.scale(left,(46,46))
iconright = transform.scale(right,(46,46))
iconup = transform.scale(up,(46,46))


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
    
def saveMap(level, fname):
    myPFile = open(fname, "wb")
    pickle.dump(level, myPFile)

screen = display.set_mode((800,600))
col = [(0,0,0),(0,255,0),(255,255,255),(255,0,0),(0,0,255),(0,255,255),(175,119,22),(255,100,100)]#nothing,can portal,cant portal,jump pad, launch pad right, launch pad left,shield 

icons = ["nothing","nothing","nothing",left,right,up]

current = 1
back = image.load("checking_level1.png")
level = loadMap("level2")
colz = (255,0,0)
buttons = [[50,True],[120,False],[190,False],[260,False],[330,False],[400,False],[470,False]]

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
            running = False

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                click = True
        if e.type == KEYDOWN:
            keys = key.get_pressed()
            if typing == True and e.key < 256:
                if keys[K_BACKSPACE]:
                    name = name[:-1]
                    
                elif keys[K_RETURN]:
                    saveMap(level, str(name))
                    typing = False
                else:
                    name += e.unicode
        if e.type == KEYUP:
            if e.key == K_ESCAPE:
                showing = not showing
                    
    mx, my = mouse.get_pos()
    keys = key.get_pressed()                
    for i in range(8):
        if keys[i+48]:
            if i < 1 or i > 7:
                pass
            else:
                current = i
                
    if click and rekt.collidepoint((mx,my)) and showing:
        typing = True

    if click and loadRect.collidepoint((mx,my)) and showing:
        loadingScreen = True
        picList = glob.glob("*")
        
        print(picList)

        
    if mouse.get_pressed()[0] and typing == False and loadingScreen == False:
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
    if typing == True:
        draw.rect(screen,(0,0,0),(0,0,600,50))
        text(name,0,0)
        
    buttons[current-1][1] = True
    
    for i in range(7):
        if buttons[i] != buttons[current-1]:
            buttons[i][1] = False
        if buttons[i][1] == False:
            colz = (255,0,0)
            
        if buttons[i][1] == True:
            colz = (0,255,0)
        if showing == True:
            draw.rect(screen,(colz),(buttons[i][0],50,50,50),3)
    if showing:           
        screen.blit(iconleft,(buttons[4][0]+2,52))
        screen.blit(iconright,(buttons[3][0]+2,52))
        screen.blit(iconup,(buttons[2][0]+2,52))
                            
        draw.rect(screen,(0,0,255),rekt)
        draw.rect(screen,(255,0,0),loadRect)
                
    if loadingScreen == True:
        for i in range(len(picList)):
            if Rect(200,50*i+200,600,50).collidepoint((mx,my)):
                if click:
                    print(picList[i])
                    level = loadMap(picList[i])
                    #print(level)
                    loadingScreen = False
                    time.sleep(0.05)
                draw.rect(screen,(255,0,0),(200,50*i+200,400,50))
                
            text(picList[i],200,50*i+200)
                       
    display.flip()

quit()
