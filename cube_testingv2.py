from pygame import *
from math import *
import time
import os
import pickle

init()

screen=display.set_mode((800,600))
running = True

brick = transform.scale(image.load('surface2.bmp'),(10,10))
block = transform.scale(image.load('block.png'),(10,10))
backg=image.load('background.bmp')
cube=transform.scale(image.load('comp_cube.png'),(20,20))
def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")
        return pickle.load(myPFile)       
    else:
        return [[0]*60 for x in range(80)]
map_grid = loadMap("level1.p")
wall_rects=[]
wall2_rects = []
blockList = []

for x in range(80):
    for y in range(60):
        c = map_grid[x][y]
        if c == 1:
            wall_rects.append(Rect((x*10,y*10,10,10)))
        if c == 2:
            wall2_rects.append(Rect((x*10,y*10,10,10)))
        if c == 3:
            blockList.append(Rect((x*10,y*10,10,10)))
            
def drawback(screen):
    'Draws the bricks/platforms of the level'
    for w in wall_rects:
        screen.blit(brick,(w[0],w[1]))
    for l in wall2_rects:
        screen.blit(block,(l[0],l[1]))
    for b in blockList:
        draw.rect(screen,(255,0,0),(b[0],b[1],10,10))

portal_state='idle'
state='idle'

pl,pw=[50,60] #player length and width
px,py=[100,450]

hit = None
hit1 = None         
grav_velocity=0 #the value that will provide constant gravity and will decide how high the player will jump

forced_end = False # [x change, y change, frames left]



click=0
portal_delay=time.time()
b_collide=False
o_collide=False
bluep=[None]
orangep=[None]
screen_p=[]

last_tp = time.time()

idle=[]
idle.append(transform.scale(image.load('1.png'),(50,70)))
idle.append(transform.scale(image.load('l1.png'),(50,70)))
forward=[]
backward=[]
frame=0
frame2=0
direction_face=0
cx,cy=300,450
for i in range(2,26):
    forward.append(transform.scale(image.load(str(i+1)+".png"),(50,70)))
for i in range(2,26):
    backward.append(transform.scale(image.load('l'+str(i+1)+".png"),(50,70)))    
def state_change(state,jump,left,right):
    if jump:
        state='jump'
    elif left or right:
        state='moving'
    else:
        state='idle'
    return state
def bullet_collideWall(portal):
    if portal != [False]:
        posRect = Rect(portal[0]-8,portal[1]-8,16,16)
        for wall in wall2_rects:
            if wall.colliderect(posRect):
                return True
                break
    return False

def cube_move(cubepos,grav_velocity,playerpos):
    'Companion Cube Movement'
    cubepos=list(cubepos)
    startpos=playerpos[:]
    if keys[K_d]:
        cubepos[0]+=2
        newpos=playerpos[:]
        cubepos=collide(startpos,newpos,map_grid)
    return cubepos
def move(playerpos,state,grav_velocity,oldpos,last_tp,forced_end,cubepos):
    '''Moves the player, including jumping. Also accounts for velocity gained from gravity.
Also includes the moving of player concerning portals.'''

    playerpos=list(playerpos)
    startpos = playerpos[:]
    
    if keys[K_d] and not forced_end:
        playerpos=list(playerpos)
        if cubepos!=None:
            if Rect(cubepos[0],cubepos[1],20,20).colliderect(Rect(playerpos[0],playerpos[1],50,50)):
                playerpos[0]+=2
                cubepos=cube_move(cubepos,grav_velocity,playerpos)
                
            else:
                playerpos[0]+=5
        else:
            playerpos[0]+=5
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        #state=state_change(state,False,True,False)
    if keys[K_a] and not forced_end:
        playerpos=list(playerpos)
        playerpos[0]-=5
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        #state=state_change(state,False,False,True)
  #  if not keys[K_a] and not keys[K_d]:
   #     state=state_change(state,False,False,False)
        

    newpos=playerpos[:]
    playerpos=collide(oldpos,newpos,map_grid)
    oldpos = playerpos[:]
    
    if state=='jump' and not forced_end: #if nothing in forced_end
        playerpos=list(playerpos)
        playerpos[1]+=grav_velocity
        grav_velocity+=0.75
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        if playerpos==oldpos and oldpos[1]<newpos[1]: #this checks if player is coming down from jump//nothing is effecting  except gravity
            state=state_change(state,False,False,False)

    elif forced_end: #True if something in it
        playerpos[0] += forced_end[0] #adds dx to px
        playerpos[1] += forced_end[1]+2 #adds dy to py
        forced_end[2] -= 1 #makes forced push smaller
        
        if forced_end[2] < 0: #ends when nothing left
            forced_end = False
    
        
    newpos=playerpos[:]
    playerpos=collide(oldpos,newpos,map_grid)

    oldpos = playerpos[:]
    
    begin_pos = playerpos[:]
    plr_x,plr_y = playerpos
    
    switched = False
    if bluep[-1] and orangep[-1] and (time.time() - last_tp>0.5 or abs(bluep[0][0]-orangep[0][0])<15) : #checks if there is a portal
        #switched = False
        outways = None
        
        if hypot(plr_x+25-bluep[0][0], plr_y+25-bluep[0][1]) < 60:
            playerpos = orangep[0]
            switched= True
            outways = orangep[-1] #direction it is facing
            
        elif hypot(plr_x+25-orangep[0][0], plr_y+25-orangep[0][1]) < 60:
            playerpos = bluep[0]
            switched= True
            outways = bluep[-1]
        
        if switched:
            last_tp = time.time()
            de_x = begin_pos[0]- startpos[0]
            de_y = begin_pos[1] - startpos[1]
            
            categories = {"Right":True, "Left":True, "Up": False, "Down": False}
            tele_adjust = {"Right": [50,-25], "Left": [-50,-25], "Up": [-25, -50], "Down": [-25, 50]}[outways]
            def rev_abs(num):
                return abs(num)*-1
            
            playerpos = [playerpos[0] + tele_adjust[0], playerpos[1] + tele_adjust[1]]
            
            quadrant_adjust = {"Right": [abs, float], "Left": [rev_abs, float], "Up": [float, rev_abs], "Down": [float, abs]}[outways] #adjusts where to teleport in quadrants

            if categories[bluep[-1]] == categories[orangep[-1]]: #Just changing one component
                

                if bluep[-1] == orangep[-1]: #Same one, inverse that component

                    ddx, ddy = quadrant_adjust[0](de_x), quadrant_adjust[1](de_y) #if on same wall got to make it push 180 the other portal
                    forced_end = [ddx, ddy, 10]

                else: #Opposite direction, keep it identical
                    forced_end = [de_x, de_y, 10] #if opposite walls just change the playerpos, no quadrant changing needed
                    
            else: #Changing both components
                de_x, de_y = de_y, de_x #Reverse them
                ddx, ddy = quadrant_adjust[0](de_x), quadrant_adjust[1](de_y) 
                forced_end = [ddx, ddy, 10]
                
    newpos=playerpos[:]
    #playerpos=collide(oldpos,newpos,map_grid)

    if not switched and collide(oldpos,[oldpos[0],oldpos[1]+1],map_grid)==[oldpos[0],oldpos[1]+1] and state!='jump': #is gravity when player isn't jumping//checks if a pixel beneath is vacant or not
        state=state_change(state,True,keys[K_d],keys[K_a])
        grav_velocity=0
    if keys[K_w] and state!='jump':
        state=state_change(state,True,keys[K_d],keys[K_a])
        grav_velocity=-8 #a negative gravity makes it go up
        
    if jumpBlock(oldpos,newpos) and keys[K_w]:
        state=state_change(state,True,keys[K_d],keys[K_a])
        grav_velocity=-20 #a negative gravity makes it go up       
        
    return playerpos,state,grav_velocity,oldpos,last_tp,forced_end,cubepos

def bullet_collide(pos):
    pos_rect=Rect(pos[0]-8,pos[1]-8,16,16)
    for wall in wall_rects:
        if wall.colliderect(pos_rect):
            return True
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
        
    for b in blockList:
        if b.colliderect(new_rect):
            return oldpos
    return newpos
def jumpBlock(oldpos,newpos):
    new_rect = Rect(newpos[0],newpos[1]+1,pl,pw)
    for b in blockList:
        if b.colliderect(new_rect):
            return True
            
    
def facing(x,y):
    if bullet_collide((x+16,y)):
        return 'Left'
    elif bullet_collide((x-16,y)):
        return 'Right'
    elif bullet_collide((x,y+16)):
        return 'Up'
    elif bullet_collide((x,y-16)):
        return 'Down'
            

def shooting(bullet, col):
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
            portal = [None]
            
        if portal != [None]:
            draw.circle(screen,col,(x_pos,y_pos),8)
            portal[-2] += 50
        
    return portal

oldpos=[px,py]
while running:
    b_click=False
    o_click=False
    keys=key.get_pressed()
    mb=mouse.get_pressed()
    mx,my=mouse.get_pos()
    for e in event.get():
        if e.type==QUIT:
            running=False
        elif e.type==MOUSEBUTTONDOWN and e.button==1:
            b_click=True
        elif e.type==MOUSEBUTTONDOWN and e.button==3:
            o_click=True
        if keys[K_d]:
            direction_face=0
        if keys[K_a]:
            direction_face=1

    screen.blit(backg,(0,0))
    drawback(screen)
    

    

#----MOVING----------------------------------
    
    (px,py),state,grav_velocity,oldpos,last_tp,forced_end,(cx,cy)=move([px,py],state,grav_velocity,oldpos,last_tp,forced_end,(cx,cy))
    

#----SHOOTING--------------------------------
    if b_click:
        bluep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]
    if (state=='idle' or state=='jump') and ((not keys[K_a] and not keys[K_d]) or (keys[K_a] and keys[K_d])):
        screen.blit(idle[direction_face],(px,py))
        
  #  if state=='moving':
   #     screen.blit(forward[frame%24],(px,py))
    #    print('hi')
    
    bluep = shooting(bluep, (8,131,219))
    
    if keys[K_r]:
        bluep=[None]
        orangep=[None]

    if o_click:
        orangep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]

    orangep = shooting(orangep, (252,69,2))
    if bluep!=[None] and orangep!=[None] :
        if portal_self_collide(bluep[0],orangep[0]):
            bluep=[None]
            orangep=[None]
    
#----DRAWING---------------------------------
    if  keys[K_d] and not keys[K_a]:
        screen.blit(forward[frame%24],(px,py))
    if keys[K_a] and not keys[K_d]:
        screen.blit(backward[frame%24],(px,py))
    #player=draw.rect(screen,(50,50,182),(px,py,pl,pw))
    #draw.rect(screen,(0,255,0),(px,py,pl,pw),3)
    if bluep[-1] != None and hit:
        draw.circle(screen,(8,131,219),[int(e) for e in bluep[0]],8)

    if orangep[-1] != None and hit1:
        draw.circle(screen,(252,69,2),[int(e) for e in orangep[0]],8)
    screen.blit(cube,(cx,cy))
    frame+=1
    oldpos=[px,py]
    display.flip()
    
quit()
            
