from pygame import *
import os
import pickle
from pprint import *
def starting():

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
    rects=[(400,(y+5)*55) for y in range(4)]
    texts=[]
    for i in range(4):
        texts.append(image.load('B%s.png'%(i+1)))

           
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return False

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(menu_background,(0,0))
        screen.blit(door,(750,455))
        screen.blit(glados,(55,0-motion))
        screen.blit(sprint[int(frame)%22],(400,500))
        for pos in range(len(rects)):
            if (Rect(rects[pos][0],rects[pos][1],208,53)).collidepoint(mpos):
                screen.blit(click_button,rects[pos])
            else:
                screen.blit(button,rects[pos])
            screen.blit(texts[pos],rects[pos])
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
    quit()
    

