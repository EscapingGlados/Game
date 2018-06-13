#LEVEL EDITOR - ESCAPE GLADOS
from pygame import *
import os
import pickle
from pprint import *
import tkinter 
showing = True
saving = Rect(750,550,50,50)
root = tkinter.Tk()
root.withdraw()
root.attributes("-topmost", True)#makes sure tk windows are priority, they would otherwise go to the back
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
<<<<<<< HEAD
    myPFile = open("tut3.p", "wb")
=======
    myPFile = open("level1.p", "wb")
>>>>>>> 767717ce2218e668dd39ea5606653ba00775e441
    pickle.dump(level, myPFile)

screen = display.set_mode((800,600))
col = [(0,0,0),(0,255,0),(255,255,255),(255,0,0),(0,0,255),(0,255,255),(175,119,22),(0,0,0)]#nothing,can portal,cant portal,jump pad, launch pad right, launch pad left 
current = 1
<<<<<<< HEAD
back = image.load("background.bmp")
level = loadMap("tut3.p")
colz = (255,0,0)
buttons = [[50,True],[120,False],[190,False],[260,False],[330,False],[400,False]]


=======
back = image.load("checking_level1.png")
level = loadMap("level1.p")
>>>>>>> 767717ce2218e668dd39ea5606653ba00775e441
running = True

while running:
    click = False
    for e in event.get():                
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                click = True
    
    mx, my = mouse.get_pos()
    keys = key.get_pressed()                
    for i in range(8):
        if keys[i+48]:
            if i < 1 or i > 6:
                pass
            else:
                current = i
    if click and saving.collidepoint((mx,my)):
        name = tkinter.filedialog.asksaveasfilename(filetypes = [("Pickle", "*.p*")])
        saveMap(level, str(name))
    if keys[K_ESCAPE] and showing == True:
        showing = False
    elif keys[K_ESCAPE] and showing == False:
        showing = True
        
    if mouse.get_pressed()[0]:
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
    
    buttons[current-1][1] = True
    
    for i in range(6):
        if buttons[i] != buttons[current-1]:
            buttons[i][1] = False
        if buttons[i][1] == False:
            colz = (255,0,0)
            
        if buttons[i][1] == True:
            colz = (0,255,0)
        if showing == True:
            draw.rect(screen,(colz),(buttons[i][0],50,50,50),3)
    draw.rect(screen,(0,0,255),saving)
    display.flip()

    
quit()
saveMap(level, "level1.p")
