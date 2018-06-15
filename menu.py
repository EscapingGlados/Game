from pygame import *
import os
import pickle
from pprint import *

def Main():
    operation = "intro"
    screen = display.set_mode((800,600))
    blitMode = 'first'
    menu_background=image.load('menu_background.png')
    door=image.load('door.png')
    glados=transform.scale(image.load('glados.png'),(248,362))
    sprint=[]
    button=image.load('button.png')
    click_button=image.load('button_on_hover.png')
    frame=0
    motion=0
    switch=True
    for i in range(2,26):
        sprint.append(transform.smoothscale(image.load(str(i+1)+'.png'),(50,70)))

    running = True
    myClock = time.Clock()
    rects=[(400,(y+5)*55) for y in range(4)]#first rects diplayes (play,create,options)
    rects2 =[(400,(y+5)*55) for y in range(3)]
    texts=[]
    texts2 = []
    coloured = []
    

    for i in range(4):
        texts.append(image.load('B%s.png'%(i+1)))
    for i in range(3):
        texts2.append(image.load('A%s.png'%(i+1)))
    for i in range(3):
        coloured.append(image.load('C%s.png'%(i+1)))
    
        
    while running:
        click = False
        for e in event.get():          
            if e.type == QUIT:
                operation = 'exit'
                running = False
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        if click and Rect(rects[0][0],rects[0][1],208,53).collidepoint(mpos) and blitMode == 'first':
            operation = 'game'
            running = False
        elif click and Rect(rects[1][0],rects[1][1],208,53).collidepoint(mpos) and blitMode == 'first':
            blitMode = 'edit'
        
        elif click and Rect(rects2[0][0],rects2[0][1],240,50).collidepoint(mpos) and blitMode == 'edit':
            operation = 'edit'
            running = False
        elif click and Rect(rects2[1][0],rects2[1][1],240,50).collidepoint(mpos) and blitMode == 'edit':
            operation = 'load'
            running = False
            
        screen.blit(menu_background,(0,0))
        screen.blit(door,(750,455))
        screen.blit(glados,(55,0-motion))
        screen.blit(sprint[int(frame)%22],(400,500))
        
 #      print(blitMode)
        if blitMode == 'first':
            for pos in range(len(rects)):
                if (Rect(rects[pos][0],rects[pos][1],208,53)).collidepoint(mpos):
                    screen.blit(click_button,rects[pos])
                else:
                    screen.blit(button,rects[pos])
                screen.blit(texts[pos],rects[pos])
                
        elif blitMode == 'edit':
            for pos in range(len(rects2)):
                if (Rect(rects2[pos][0],rects2[pos][1],240,50)).collidepoint(mpos):
                    screen.blit(coloured[pos],rects2[pos])
                else:
                    screen.blit(texts2[pos],rects2[pos])
 #               screen.blit(texts2[pos],rects2[pos]) 
            
        frame+=0.7
        if switch:
            motion+=1
            if motion==41:
                switch=False
        if switch==False:
            motion-=1
            if motion==-2:
                switch=True
        

                    
        display.flip()
    return operation



