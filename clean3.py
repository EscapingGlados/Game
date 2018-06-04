from pygame import *
from math import *
import time as t
screen=display.set_mode((800,600))
running = True

brick = image.load('surface2.bmp')
brick=transform.scale(brick,(25,25))
backg=image.load('background.bmp')

map_grid=open("text_mask.txt").read().strip().split("\n")

wall_rects=[]

#appends rects and positions
def loadMap(map_grid):
    'Loads in the rects of the map, detecting collission'
    wall_rects=[]
    for x in range(len(map_grid)):
        for y in range(len(map_grid[x])):
            if map_grid[x][y]=='w':
                wall_rects.append(Rect(y*25,x*25,25,25))
    return wall_rects

wall_rects=loadMap(map_grid)

def drawback(screen):
    'Draws the bricks/platforms of the level'
    for w in wall_rects:
        screen.blit(brick,(w[0],w[1]))


portal_stateb='idle'
portal_stateo='idle'
state='idle'

pl,pw=[50,50] #player length and width
px,py=[100,450]
player = draw.rect(screen,(50,50,182),(px,py,pl,pw))

grav_velocity=0 #the value that will provide constant gravity and will decide how high the player will jump

click=0
portal_delay=t.time()
b_collide=False
o_collide=False
bluep=[False]
orangep=[False]
screen_p=[]

def move(playerpos):
    global state #needs to be global since state will be changing a lot (player state)
    global grav_velocity #will be changing frequently//jumping and gravity
    'Moves the player, including jumping. Also accounts for velocity gained from gravity'
    oldpos=[px,py] #records current position which will be old once player starts moving
    if keys[K_d]: #if player presses the key 'D'
        playerpos=list(playerpos) #changes the tuple to be mutable
        playerpos[0]+=5 #moves 5 pixels right
        newpos=playerpos[:] #records the new player position
        playerpos=collide(oldpos,newpos,map_grid) #checks which of the positions doesn't collide, and makes the player position the most valid one
    if keys[K_a]: #SAME AS ABOVE JUST MOVES LEFT
        playerpos=list(playerpos)
        playerpos[0]-=5
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
    oldpos=playerpos[:] #updates current position to be the old one

    if collide(oldpos,[oldpos[0],oldpos[1]+1],map_grid)==[oldpos[0],oldpos[1]+1] and state!='jump': #is gravity when player isn't jumping//checks if a pixel beneath is vacant or not
        state='jump' #state is jump
        grav_velocity=0
    if keys[K_w] and state!='jump':
        state='jump'
        grav_velocity=-8 #a negative gravity makes it go up
    if state=='jump':
        playerpos=list(playerpos)
        playerpos[1]+=grav_velocity
        grav_velocity+=0.4
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        if playerpos==oldpos and oldpos[1]<newpos[1]: #this checks if player is coming down from jump//nothing is effecting  except gravity
            state='idle'
    return playerpos
def bullet_collide(pos):
    pos_rect=Rect(pos[0]-8,pos[1]-8,16,16)
    for wall in wall_rects:
        if wall.colliderect(pos_rect):
            return True
    return False
def collide(oldpos,newpos,grid):
    'Checks if the new position is vacant, if not, will return the old position'
    new_rect=Rect(newpos[0],newpos[1],pl,pw)
    for wall in wall_rects:
        if wall.colliderect(new_rect):
            return oldpos
    return newpos



while running:
    b_click=False
    o_click=False
    for e in event.get():
        if e.type==QUIT:
            running=False
        if e.type==MOUSEBUTTONDOWN and e.button==1:
            b_click=True
        if e.type==MOUSEBUTTONDOWN and e.button==3:
            o_click=True

    screen.blit(backg,(0,0))
    drawback(screen)


    keys=key.get_pressed()
    mb=mouse.get_pressed()
    mx,my=mouse.get_pos()

#----MOVING----------------------------------
    px,py=move([px,py])

#----SHOOTING--------------------------------


    if b_click:
        bluep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,True]
    if bluep[-1]:
        distance = bluep[-2]
        x_pos = int(bluep[0][0]+distance*cos(bluep[-3]))
        y_pos = int(bluep[0][1]+distance*sin(bluep[-3]))
        if bullet_collide([x_pos,y_pos]):
            changes = 1
            while True:
                x = int(x_pos - cos(bluep[-3])*changes)
                y = int(y_pos - sin(bluep[-3])*changes)
                changes+=1
                if bullet_collide([x,y]) ==False:
                    bluep[-1]=False
                    break
        draw.circle(screen,(8,131,219),(x_pos,y_pos),16)
        bluep[-2]+=50
    elif not bluep[-1] and len(bluep)>1:
        draw.circle(screen,(8,131,219),(x,y),16)
    if keys[K_r]:
        bluep=[False]
        orangep=[False]



    if o_click:
        orangep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,True]
    if orangep[-1]:
        distance = orangep[-2]
        x_pos = int(orangep[0][0]+distance*cos(orangep[-3]))
        y_pos = int(orangep[0][1]+distance*sin(orangep[-3]))
        if bullet_collide([x_pos,y_pos]):
            changes = 1
            while True:
                x2 = int(x_pos - cos(orangep[-3])*changes)
                y2= int(y_pos - sin(orangep[-3])*changes)
                changes+=1
                if bullet_collide([x2,y2]) ==False:
                    orangep[-1]=False
                    break
        draw.circle(screen,(252,69,2),(x_pos,y_pos),16)
        orangep[-2]+=50




    draw.rect(screen,(0,255,0),Rect(px,py,50,50),2)
    if bluep[-1] and len(bluep)>1:

       # if Rect(x-16,y-16,32,32).colliderect(Rect(px,py,50,50)):
            if portal_stateo=='right':
                px=x2+25
                py=y2
            if portal_stateo=='left':
                px=x2-25
                py=y2
            if portal_stateo=='down':
                px=x2-25
                py=y2
            if portal_stateo=='down':
                px=x2-25
                py=y2

#----DRAWING---------------------------------

    player=draw.rect(screen,(50,50,182),(px,py,pl,pw))


    if bluep[-1]==False and len(bluep)>1:
        if bullet_collide((x+16,y)):
            portal_stateb='left'
        elif bullet_collide((x-16,y)):
            portal_stateb='right'
        elif bullet_collide((x,y+16)):
            portal_stateb='up'
        elif bullet_collide((x,y-16)):
            portal_stateb='down'


    if orangep[-1]==False and len(orangep)>1:
        if bullet_collide((x2+16,y2)):
            portal_stateo='left'
        elif bullet_collide((x2-16,y2)):
            portal_stateo='right'
        elif bullet_collide((x2,y2+16)):
            portal_stateo='up'
        elif bullet_collide((x2,y2-16)):
            portal_stateo='down'
        draw.circle(screen,(252,69,2),(x2,y2),16)

    display.flip()
quit()

