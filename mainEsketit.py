#main game
from pygame import *
import os
import pickle
from math import *
import time
import glob
##from MAIN import *
##
##from menu import *
##
##from LEVELEDIT import *

screen=display.set_mode((800,600))

def game():

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
    launchPad = []#right shooting
    launchPad2 = []#left shooting
    shield = []#blue shields

    for x in range(80):
        for y in range(60):
            c = map_grid[x][y]
            if c == 1:
                wall_rects.append(Rect((x*10,y*10,10,10)))#nonclickable
            if c == 2:
                wall2_rects.append(Rect((x*10,y*10,10,10)))#clickable
            if c == 3:
                blockList.append(Rect((x*10,y*10,10,10)))#jump slime
            if c == 4:
                launchPad.append(Rect((x*10,y*10,10,10)))#launchpadright
            if c == 5:
                launchPad2.append(Rect((x*10,y*10,10,10)))#launchpadleft
            if c == 6:
                shield.append(Rect((x*10,y*10,10,10)))
            
                
                
    def drawback(screen):
        'Draws the bricks/platforms of the level'
        for w in wall_rects:
            screen.blit(brick,(w[0],w[1]))
        for l in wall2_rects:
            screen.blit(block,(l[0],l[1]))
        for b in blockList:
            draw.rect(screen,(255,0,0),(b[0],b[1],10,10))
        for p in launchPad:
            draw.rect(screen,(65,65,65),(p[0],p[1],10,10))
        for x in launchPad2:
            draw.rect(screen,(0,0,255),(x[0],x[1],10,10))
        for s in shield:
            draw.rect(screen,(0,255,255),(s[0],s[1],10,10))        

    portal_state='idle'
    state='idle'
    mode = 'idle'

    pl,pw=[50,60] #player length and width
    px,py=[100,450]

    hit = None
    hit1 = None         
    grav_velocity=0 #the value that will provide constant gravity and will decide how high the player will jump
    xchange = 0
    forced_end = False # [x change, y change, frames left]
    floatingmode = False

    click=0
    portal_delay=time.time()
    b_collide=False
    o_collide=False
    bluep=[None]
    orangep=[None]
    screen_p=[]
    changing = 0

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
    face = None
    for i in range(2,26):
        forward.append(transform.scale(image.load(str(i+1)+".png"),(50,70)))
    for i in range(2,26):
        backward.append(transform.scale(image.load('l'+str(i+1)+".png"),(50,70)))    
    def state_change(state,jump,left,right):
        global mode
        if jump:
            state='jump'
        elif left or right:
            state='moving'
        else:
            state='idle'
            mode = 'idle'
        return state
    def bullet_collideWall(portal):
        if portal != [False]:
            posRect = Rect(portal[0]-8,portal[1]-8,16,16)
            for wall in wall2_rects:
                if wall.colliderect(posRect):
                    return True
                    break
        return False

    def shieldCollide(portal):
        if portal != [False]:
            posRect = Rect(portal[0]-8,portal[1]-8,16,16)
            for p in shield:
                if p.colliderect(posRect):
                    return True
                    break
        return False
    def playerCol(pos):
        posRect = Rect(pos[0],pos[1],pl,pw)
        for s in shield:
            if s.colliderect(posRect):
                return True
                break
        return False
    def move(playerpos,state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing):
        '''Moves the player, including jumping. Also accounts for velocity gained from gravity.
    Also includes the moving of player concerning portals.'''
        
        playerpos=list(playerpos)
        startpos = playerpos[:]
        
        if keys[K_d] and not forced_end: #and mode != "launchingright" and mode != "launchingleft":
            playerpos=list(playerpos)
            playerpos[0]+=5
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid)

        if keys[K_a] and not forced_end:# and mode != "launchingright" and mode != "launchingleft":
            playerpos=list(playerpos)
            playerpos[0]-=5
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid)

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
            playerpos[1] += forced_end[1] #adds dy to py
            forced_end[2] -= 1 #makes forced push smaller
            
            if forced_end[2] < 0: #ends when nothing left
                forced_end = False
                floatingmode = True
        if floatingmode == True:
            if face == "Right":
                playerpos[0] += 15
            elif face == "Left":
                playerpos[0] -= 15         
        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid)

        oldpos = playerpos[:]
        
        begin_pos = playerpos[:]
        plr_x,plr_y = playerpos
        
        switched = False
        if bluep[-1] and orangep[-1] and (time.time() - last_tp>0.5 or abs(bluep[0][0]-orangep[0][0])<15) : #checks if there is a portal
            #switched = False
            outways = None
            
            if hypot(plr_x+25-bluep[0][0], plr_y+25-bluep[0][1]) < 49:
                playerpos = orangep[0]
                switched= True
                outways = orangep[-1] #direction it is facing
                
            elif hypot(plr_x+25-orangep[0][0], plr_y+25-orangep[0][1]) < 49:
                playerpos = bluep[0]
                switched= True
                outways = bluep[-1]
            
            if switched:
                last_tp = time.time()
                de_x = begin_pos[0]- startpos[0]
                de_y = begin_pos[1] - startpos[1]
                
                categories = {"Right":True, "Left":True, "Up": False, "Down": False}
                tele_adjust = {"Right": [50,-25], "Left": [-50,-25], "Up": [-25, -50], "Down": [-25, 50]}[outways]

                
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


                if outways != None:
                    face = outways
                

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
            
        if launch(oldpos,newpos) == 'right':
            grav_velocity = -20
            xchange = -20
            mode = 'launchingright'
        if launch(oldpos,newpos) == 'left':
            grav_velocity = -20
            xchange = -20
            mode = 'launchingleft'
            
        if mode =='launchingright': #if nothing in forced_end
            playerpos=list(playerpos)
            playerpos[1] += grav_velocity
            playerpos[0] -= xchange
            grav_velocity+=0.75
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid)
            
        if mode == 'launchingleft':
            playerpos=list(playerpos)
            playerpos[1] += grav_velocity
            playerpos[0] += xchange
            grav_velocity+=0.75
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid)
            
        return playerpos,state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing

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

    def rev_abs(num):
        return abs(num)*-1
    def collide(oldpos,newpos,grid):
        'Checks if the new position is vacant, if not, will return the old position'
        global floatingmode
        new_rect=Rect(newpos[0],newpos[1],pl,pw)
        
        for wall in wall_rects:
            if wall.colliderect(new_rect):
                floatingmode = False
                return oldpos
            
        for x in wall2_rects:
            if x.colliderect(new_rect):
                floatingmode = False

                return oldpos
            
        for b in blockList:
            if b.colliderect(new_rect):
                floatingmode = False

                return oldpos

        for p in launchPad:
            if p.colliderect(new_rect):
                floatingmode = False

                return oldpos
            
        for x in launchPad2:
            if x.colliderect(new_rect):
                floatingmode = False

                return oldpos
        return newpos

    def jumpBlock(oldpos,newpos):
        
        new_rect = Rect(newpos[0],newpos[1]+1,pl,pw)
        for b in blockList:
            if b.colliderect(new_rect):
                return True
    def launch(oldpos,newpos):
        new_rect = Rect(newpos[0],newpos[1]+2,pl,pw)
        for p in launchPad:
            if p.colliderect(new_rect):
                return 'right'
            
        for x in launchPad2:
            if x.colliderect(new_rect):
                return 'left'

            
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
            if shieldCollide([x_pos,y_pos]):
                portal = [None]
                
            if portal != [None]:
                draw.circle(screen,col,(x_pos,y_pos),8)
                portal[-2] += 50#adding to distance
            
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
        
        (px,py),state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing=move([px,py],state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing)
        

    #----SHOOTING--------------------------------
        if b_click:
            bluep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]
        if (state=='idle' or state=='jump') and ((not keys[K_a] and not keys[K_d]) or (keys[K_a] and keys[K_d])):
            screen.blit(idle[direction_face],(px,py))
            
        
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
            if shieldCollide((px,py)):
                bluep=[None]
                orangep=[None]           
    #----DRAWING---------------------------------
        if  keys[K_d] and not keys[K_a]:
            screen.blit(forward[frame%24],(px,py))
        if keys[K_a] and not keys[K_d]:
            screen.blit(backward[frame%24],(px,py))

        if bluep[-1] != None and hit:
            draw.circle(screen,(8,131,219),[int(e) for e in bluep[0]],8)

        if orangep[-1] != None and hit1:
            draw.circle(screen,(252,69,2),[int(e) for e in orangep[0]],8)
        screen.blit(cube,(cx,cy))
        frame+=1
        oldpos=[px,py]
        display.flip()
    quit()
        
def levelEd():


    showing = True
    typing = False
    loadingScreen = False
    font.init()
    rekt = Rect(750,550,50,50)
    loadRect = Rect(700,550,50,50)

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
        myPFile = open("Saves/"+fname, "wb")
        pickle.dump(level, myPFile)

    screen = display.set_mode((800,600))
    col = [(0,0,0),(0,255,0),(255,255,255),(255,0,0),(0,0,255),(0,255,255),(175,119,22),(0,0,0)]#nothing,can portal,cant portal,jump pad, launch pad right, launch pad left 
    current = 1
    back = image.load("background.bmp")
    level = loadMap("level1.p")
    colz = (255,0,0)
    buttons = [[50,True],[120,False],[190,False],[260,False],[330,False],[400,False]]

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
                        
        mx, my = mouse.get_pos()
        keys = key.get_pressed()                
        for i in range(8):
            if keys[i+48]:
                if i < 1 or i > 6:
                    pass
                else:
                    current = i
                    
        if click and rekt.collidepoint((mx,my)):
            typing = True

        if click and loadRect.collidepoint((mx,my)):
            loadingScreen = True
            picList = glob.glob("Saves/*")
            
                
            print(picList)

        if keys[K_ESCAPE] and showing == True:
            showing = False

        
        elif keys[K_ESCAPE] and showing == False:
            showing = True
            
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
        
        for i in range(6):
            if buttons[i] != buttons[current-1]:
                buttons[i][1] = False
            if buttons[i][1] == False:
                colz = (255,0,0)
                
            if buttons[i][1] == True:
                colz = (0,255,0)
            if showing == True:
                draw.rect(screen,(colz),(buttons[i][0],50,50,50),3)
        draw.rect(screen,(0,0,255),rekt)
        draw.rect(screen,(255,0,0),loadRect)
                    
        if loadingScreen == True:
            for i in range(len(picList)):
                if Rect(200,50*i+200,600,50).collidepoint((mx,my)):
                    if click:
                        print(picList[i][6:]+".p")
                        level = loadMap(picList[i][6:]+".p")
                       # print(level)
                        loadingScreen = False
                        time.sleep(0.05)
                    draw.rect(screen,(255,0,0),(200,50*i+200,400,50))
                    
                text(picList[i][6:],200,50*i+200)
                           
        display.flip()

    quit()

def starting():
    global gameType
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
    rects=[(400,(y+5)*55) for y in range(4)]
    print(rects)
    texts=[]
    for i in range(4):
        texts.append(image.load('B%s.png'%(i+1)))

           
    while running:
        click = False
        for e in event.get():          
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

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
        
        if (Rect(rects[0][0],rects[0][1],208,53)).collidepoint(mpos) and click:
            running = False
            game()
            break
        if (Rect(rects[1][0],rects[1][1],208,53)).collidepoint(mpos) and click:
            running = False
            levelEd()
            break
    
        display.flip()
    quit()

starting()
