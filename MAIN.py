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

def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")
        return pickle.load(myPFile)       
    else:
        return [[0]*60 for x in range(80)]
map_grid = loadMap("level1.p")
wall_rects=[]
wall2_rects = [] 

for x in range(80):
    for y in range(60):
        c = map_grid[x][y]
        if c == 1:
            wall_rects.append(Rect((x*10,y*10,10,10)))
        if c == 2:
            wall2_rects.append(Rect((x*10,y*10,10,10)))
            
def drawback(screen):
    'Draws the bricks/platforms of the level'
    for w in wall_rects:
        screen.blit(brick,(w[0],w[1]))
    for l in wall2_rects:
        screen.blit(block,(l[0],l[1]))

portal_state='idle'
state='idle'

pl,pw=[50,50] #player length and width
px,py=[100,450]
player = draw.rect(screen,(50,50,182),(px,py,pl,pw))
            
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
forward=[]
frame=0
for i in range(2,26):
    forward.append(transform.scale(image.load(str(i+1)+".png"),(50,70)))
    
def state_change(state,jump,left,right):
    if jump:
        state='jump'
    elif left or right:
        state='moving'
    else:
        state='idle'
    return state

def move(playerpos,state,grav_velocity,oldpos,last_tp,forced_end):
    '''Moves the player, including jumping. Also accounts for velocity gained from gravity.
Also includes the moving of player concerning portals.'''

    playerpos=list(playerpos)
    startpos = playerpos[:]
    if keys[K_a] or keys[K_d]:
        screen.blit(forward[frame%24],playerpos)
    if keys[K_d]:
        playerpos=list(playerpos)
        playerpos[0]+=5
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        #state=state_change(state,False,True,False)
    if keys[K_a]:
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
    
    if state=='jump' and not forced_end:
        playerpos=list(playerpos)
        playerpos[1]+=grav_velocity
        grav_velocity+=0.4
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)
        if playerpos==oldpos and oldpos[1]<newpos[1]: #this checks if player is coming down from jump//nothing is effecting  except gravity
            state=state_change(state,False,False,False)
    elif forced_end:
        playerpos[0] += forced_end[0]
        playerpos[1] += forced_end[1]
        forced_end[2] -= 0.75
        if forced_end[2] <= 0:
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
        
        if hypot(plr_x+25-bluep[0][0], plr_y+25-bluep[0][1]) < 50:
            playerpos = orangep[0]
            switched= True
            outways = orangep[-1] #direction it is facing
            
        elif hypot(plr_x+25-orangep[0][0], plr_y+25-orangep[0][1]) < 50:
            playerpos = bluep[0]
            switched= True
            outways = bluep[-1]
        
        if switched:
            last_tp = time.time()
            de_x = begin_pos[0]- startpos[0]
            de_y = begin_pos[1] - startpos[1]
            
            categories = {"Right":True, "Left":True, "Up": False, "Down": False}
            bonuses = {"Right": [50,-25], "Left": [-50,-25], "Up": [-25, -50], "Down": [-25, 50]}[outways]
            def rev_abs(num):
                return abs(num)*-1
            
            playerpos = [playerpos[0] + bonuses[0], playerpos[1] + bonuses[1]]
            
            good_funcs = {"Right": [abs, float], "Left": [rev_abs, float], "Up": [float, rev_abs], "Down": [float, abs]}[outways] #adjusts where to teleport in quadrants

            if categories[bluep[-1]] == categories[orangep[-1]]: #Just changing one component
                

                if bluep[-1] == orangep[-1]: #Same one, inverse that component

                    ddx, ddy = good_funcs[0](de_x), good_funcs[1](de_y)
                    forced_end = [ddx, ddy, 10]

                else: #Opposite direction, keep it identical
                    forced_end = [de_x, de_y, 10]
                    
            else: #Changing both components
                de_x, de_y = de_y, de_x #Reverse them
                ddx, ddy = good_funcs[0](de_x), good_funcs[1](de_y)
                forced_end = [ddx, ddy, 10]
                
    newpos=playerpos[:]
    #playerpos=collide(oldpos,newpos,map_grid)

    if not switched and collide(oldpos,[oldpos[0],oldpos[1]+1],map_grid)==[oldpos[0],oldpos[1]+1] and state!='jump': #is gravity when player isn't jumping//checks if a pixel beneath is vacant or not
        state=state_change(state,True,keys[K_d],keys[K_a])
        grav_velocity=0
    if keys[K_w] and state!='jump' :
        state=state_change(state,True,keys[K_d],keys[K_a])
        grav_velocity=-8 #a negative gravity makes it go up
    
    return playerpos,state,grav_velocity,oldpos,last_tp,forced_end

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
        
    for x in wall2_rects:
        if x.colliderect(new_rect):
            return oldpos
        
    return newpos

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
                    break
                
        draw.circle(screen,col,(x_pos,y_pos),16)
        portal[-2] += 50
        
    return portal

oldpos=[px,py]
while running:
    b_click=False
    o_click=False
    for e in event.get():
        if e.type==QUIT:
            running=False
        elif e.type==MOUSEBUTTONDOWN and e.button==1:
            b_click=True
        elif e.type==MOUSEBUTTONDOWN and e.button==3:
            o_click=True

    screen.blit(backg,(0,0))
    drawback(screen)
    

    keys=key.get_pressed()
    mb=mouse.get_pressed()
    mx,my=mouse.get_pos()

#----MOVING----------------------------------
    
    (px,py),state,grav_velocity,oldpos,last_tp,forced_end=move([px,py],state,grav_velocity,oldpos,last_tp,forced_end)

#----SHOOTING--------------------------------
    if b_click:
        bluep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]
    if (state=='idle' or state=='jump') and not keys[K_a] and not keys[K_d]:
        screen.blit(idle[frame%1],(px,py))
        
    if state=='moving':
        screen.blit(forward[frame%24],(px,py))
        print('hi')
    
    bluep = shooting(bluep, (8,131,219))
    
    if keys[K_r]:
        bluep=[False]
        orangep=[False]

    if o_click:
        orangep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]

    orangep = shooting(orangep, (252,69,2))
#----DRAWING---------------------------------
    
    #player=draw.rect(screen,(50,50,182),(px,py,pl,pw))

    if bluep[-1] != None:
        draw.circle(screen,(8,131,219),[int(e) for e in bluep[0]],16)

    if orangep[-1] != None:
        draw.circle(screen,(252,69,2),[int(e) for e in orangep[0]],16)
    frame+=1
    oldpos=[px,py]
    display.flip()
    
quit()
            
