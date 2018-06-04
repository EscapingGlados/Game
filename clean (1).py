from pygame import *
from math import *
import time
import os
import pickle
init()
screen=display.set_mode((800,600))
running = True

brick = transform.scale(image.load('surface2.bmp'),(25,25))
block = transform.scale(image.load('block.png'),(25,25))
backg=image.load('background.bmp')


#dfsdfklsdnfasjfnasldnasdnasldknasklnalfknsadklasndlkasdn
#testing github stuffffffff
#milk me
def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")
        return pickle.load(myPFile)       
    else:
        return [[0]*24 for x in range(32)]
map_grid = loadMap("level1.p")
wall_rects=[]
wall2_rects = []
oldpos = [100,450]

for x in range(32):
    for y in range(24):
        c = map_grid[x][y]
        if c == 1:
            wall_rects.append(Rect((x*25,y*25,25,25)))
        if c == 2:
            wall2_rects.append(Rect((x*25,y*25,25,25)))
def drawback(screen):
    'Draws the bricks/platforms of the level'

    for w in wall_rects:
        screen.blit(brick,(w[0],w[1]))
    for l in wall2_rects:
        screen.blit(block,(l[0],l[1]))
        
portal_state='idle'
state='idle'
col = [(255,0,0),(0,255,0),(255,255,255),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
pl,pw=[50,50] #player length and width
px,py=[100,450]
player = draw.rect(screen,(50,50,182),(px,py,pl,pw))
hit = None
hit1 = None
switch = None

grav_velocity=0 #the value that will provide constant gravity and will decide how high the player will jump

click=0
portal_delay=time.time()
b_collide=False
o_collide=False
bluep=[False]
orangep=[False]
dir_adjust={'left':[-65,-25],'right':[35,-25],'up':[-25,-65],'down':[-25,35]}
screen_p=[]

def move(playerpos):
    'Moves the player, including jumping. Also accounts for velocity gained from gravity'
    global state
    global grav_velocity
    oldpos=[px,py]
    
    if keys[K_d]:
        playerpos=list(playerpos)
        playerpos[0]+=5
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        
    if keys[K_a]:
        playerpos=list(playerpos)
        playerpos[0]-=5
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)

    if collide(oldpos,[oldpos[0],oldpos[1]+1],map_grid)==[oldpos[0],oldpos[1]+1] and state!='jump': #is gravity when player isn't jumping//checks if a pixel beneath is vacant or not
        state='jump'
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

def bullet_collideWall(portal):
    if portal != [False]:
        posRect = Rect(portal[0]-8,portal[1]-8,16,16)
        for wall in wall2_rects:
            if wall.colliderect(posRect):
                return True
                break
    return False

def portal_self_collide(portal1,portal2):
    p1_rect=Rect(portal1[0]-8,portal1[1]-8,16,16)
    p2_rect=Rect(portal2[0]-8,portal2[1]-8,16,16)
    if p1_rect.colliderect(p2_rect):
        return [False]
    
    

def collide(oldpos,newpos,grid):
    'Checks if the new position is vacant, if not, will return the old position'
    new_rect=Rect(newpos[0],newpos[1],pl,pw)
    
    for wall in wall_rects:
        if wall.colliderect(new_rect):
            return oldpos
        
    for x in wall2_rects:
        if x.colliderect(new_rect):
            return oldpos
        
    return newpos
def portalCollide(pos,bpos,opos):
    if hypot(pos[0]+25 - bpos[0],pos[1]+25 - bpos[1]) < 35:
        return "bSwitch"
    if hypot(pos[0]+25 - opos[0],pos[1]+25 - opos[1]) < 35:
        return "oSwitch"


def facing(x,y):
    if bullet_collide((x+16,y)):
        return 'left'
    elif bullet_collide((x-16,y)):
        return 'right'
    elif bullet_collide((x,y+16)):
        return 'up'
    elif bullet_collide((x,y-16)):
        return 'down'
    
def shooting(bullet, col):#bluep or orangep,colour
    global hit,hit1
    
    portal = bullet[:]
    if portal[-1] == None and portal != [None]:
        distance = portal[-2]
        x_pos = int(portal[0][0]+distance*cos(portal[-3]))
        y_pos = int(portal[0][1]+distance*sin(portal[-3]))
        if bullet_collide([x_pos,y_pos]):
            changes = 1
            while True:
                x = int(x_pos - cos(portal[-3])*changes)
                y = int(y_pos - sin(portal[-3])*changes)
                changes+=1
                if bullet_collide([x,y]) == False:
                    portal[-1] = facing(x,y)
                    portal[0] = [x,y]
                    if col == (8,131,219):
                       hit = True
                    elif col == (252,69,2):
                        hit1 = True
                    break
        if bullet_collideWall([x_pos,y_pos]):
            portal = [False]
            
        if portal != [False]:
            draw.circle(screen,col,(x_pos,y_pos),16)
            portal[-2] += 50
        
    return portal

def angle_finder(bx,by,ox,oy,b_direction,o_direction):#portal coordinates,portal facing
    theta=degrees(atan2(oy-by,0)-atan2(0,bx-ox))
    if (b_direction=='up' or b_direction=='down') and (o_direction=='up' or o_direction=='down') :
        if b_direction==o_direction:
            theta=180
        else:
            theta=0
    if (b_direction=='left' or b_direction=='right') and (o_direction=='left' or o_direction=='right'):
        if b_direction==o_direction:
            theta=180
        else:
            theta=0
    return theta*-1

    
def dXdY(oldx,oldy,portalx,portaly,portal2x,portal2y):
    dist = 1
    angle = atan2(oldy-portaly,oldx-portalx)
    dx = int(portal2x+dist*cos(angle))
    dy = int(portal2y+dist*sin(angle))
    dist += 10
    return [dx,dy]
while running:
    ox,oy=px,py
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
        hit = None
        bluep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]
    
    bluep = shooting(bluep, (8,131,219))
    if keys[K_r]:
        bluep=[False]
        orangep=[False]

    if o_click:
        hit1 = None
        orangep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]

    orangep = shooting(orangep, (252,69,2))

    if bluep!=[False] and orangep!=[False] and (hit or hit1):
        if portal_self_collide(bluep[0],orangep[0]):
            bluep=[False]
            orangep=[False]
            
    if bluep != [False] and orangep != [False] and hit and hit1:
        switch = portalCollide([px,py],bluep[0],orangep[0])
        
        if switch == "oSwitch":
            flying = True

        elif switch == "bSwitch":
            px = dXdY(oldpos[0],oldpos[1],bluep[0][0],bluep[0][1],orangep[0][0],orangep[0][1])[0]
            py = dXdY(oldpos[0],oldpos[1],bluep[0][0],bluep[0][1],orangep[0][0],orangep[0][1])[1]
    if flying:
        px = dXdY(px,py,orangep[0][0],orangep[0][1],bluep[0][0],bluep[0][1])[0]
        py = dXdY(px,py,orangep[0][0],orangep[0][1],bluep[0][0],bluep[0][1])[1]
#----DRAWING---------------------------------

    player=draw.rect(screen,(50,50,182),(px,py,pl,pw))

    if bluep[-1] != False and hit == True:
        draw.circle(screen,(8,131,219),[int(e) for e in bluep[0]],16)

    if orangep[-1] != False and hit1 == True:
        draw.circle(screen,(252,69,2),[int(e) for e in orangep[0]],16)
           
    oldpos=[px,py]
    display.flip()
quit()
            
