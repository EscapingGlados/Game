from pygame import *
from math import *
import time as t
import os
import pickle

def Main():
    running = True
    screen = display.set_mode((800,600))

    brick = transform.scale(image.load('surface2.bmp'),(10,10))
    block = transform.scale(image.load('block.png'),(10,10))
    level1=image.load('Level_1_final.png')
    level2=image.load('Level_2_final.png')
    level3=image.load('Level_3_final.png')
    level4=image.load('Level_4_final.png')
    level5=image.load('Level_5_final.png')
    
    cube=transform.scale(image.load('comp_cube.png'),(20,20))
    bluep_sprite=[]
    for i in range(4):
        bluep_sprite.append(transform.scale(image.load('bp%s.png'%(i)),(48,30)))
    blue_frame=0

    orangep_sprite=[]
    for i in range(4):
        orangep_sprite.append(transform.scale(image.load('op%s.png'%(i)),(48,30)))
    orange_frame=0
    def loadMap(fname):
        if fname in os.listdir("."):
            myPFile = open(fname, "rb")
            return pickle.load(myPFile)       
        else:
            return [[0]*60 for x in range(80)]


    levels = ["level1Real","level2","level3.p","level4.p","level5.p"]
    levelindex = 0
    
    map_grid = loadMap(levels[levelindex])
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
            if c == 7:
                endpoint = [x*10,y*10]
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
    portal_delay=t.time()
    b_collide=False
    o_collide=False
    bluep=[None]
    orangep=[None]
    screen_p=[]
    changing = 0

##    def drawback(screen):
##        'Draws the bricks/platforms of the level'
##        for w in wall_rects:
##            screen.blit(brick,(w[0],w[1]))
##        for l in wall2_rects:
##            screen.blit(block,(l[0],l[1]))
##        for b in blockList:
##            draw.rect(screen,(255,0,0),(b[0],b[1],10,10))
##        for p in launchPad:
##            draw.rect(screen,(65,65,65),(p[0],p[1],10,10))
##        for x in launchPad2:
##            draw.rect(screen,(0,0,255),(x[0],x[1],10,10))
##        for s in shield:
##            draw.rect(screen,(0,255,255),(s[0],s[1],10,10))
##        draw.rect(screen,(255,100,100),(endpoint[0],endpoint[1],10,10))

    def reset(wall_rects,wall2_rects,blockList,launchPad,launchPad2,shield,mode,portal_state,state,hit,hit1,grav_velocity,xchange,forced_end,floatingmode,px,py):

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
                if c == 7:
                    endpoint = [x*10,y*10]
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

        return wall_rects,wall2_rects,blockList,launchPad,launchPad2,shield,mode,portal_state,state,hit,hit1,grav_velocity,xchange,forced_end,floatingmode,px,py
        
    last_tp = t.time()

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
    def state_change(state,jump,left,right,mode):
        if jump:
            state='jump'
        elif left or right:
            state='moving'
        else:
            state='idle'
            mode = 'idle'
        return state,mode
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
    grav_velocity2=0
    cube_state='idle'
    cx,cy=280,240
    opos=[cx,cy]
    cube_last_tp=t.time()
    cube_forced_end=False
    cube_mode='idle'
    c_xchange=0
    cube_floatingmode=False
    holding=False
    def cubemove(cubepos,cube_state,grav_velocity2,opos,cube_last_tp,cube_forced_end,cube_mode,c_xchange,cube_floatingmode,holding):
        
        cubepos=list(cubepos)
        cube_startpos=cubepos[:]
        npos=cubepos[:]
        cubepos=collide(opos,npos,map_grid,floatingmode,20,20,20,20)
       
        opos=cubepos[:]
  
        if holding==True:
            grav_velocity2=0
        if cube_state=='falling' and holding==False:
 
            cubepos=list(cubepos)
            cubepos[1]+=grav_velocity2
            grav_velocity2+=0.75
            
            npos=cubepos[:]
            
    
            cubepos=collide(opos,npos,map_grid,floatingmode,20,20,20,20)
            
            if cubepos==opos and opos[1]<npos[1] and cube_state=='falling':
                cube_state='idle'
                cube_mode='idle'
        
        if collide(opos,[opos[0],opos[1]+1],map_grid,floatingmode,20,20,20,20)==[opos[0],opos[1]+1] and cube_state!='falling' :
            cube_state='falling'
            grav_velocity2=0
            
        if jumpBlock(opos,npos,20,20) and cube_state=='idle' :
            cube_state='bounce'
            grav_velocity2=0
            
        opos=cubepos[:]
      
        if cube_state=='bounce':
            cubepos=list(cubepos)
            cubepos[1]+=grav_velocity2
        
            grav_velocity2-=70.5
           
        
            npos=cubepos[:]
            cubepos=collide(opos,npos,map_grid,floatingmode,20,20,20,20)
           
            if cubepos==opos and opos[1]<npos[1]: #this checks if player is coming down from jump//nothing is effecting  except gravity
                cube_state='idle'

            
            cubepos=collide(opos,npos,map_grid,floatingmode,20,20,20,20)
        opos = cubepos[:]
        cube_begin_pos = cubepos[:]
       
        c_plr_x,c_plr_y = cubepos
        cube_switched = False
        if bluep[-1] and orangep[-1] and (t.time() - cube_last_tp>0.5 or abs(bluep[0][0]-orangep[0][0])<15) : #checks if there is a portal
            #switched = False
            cube_outways = None
    ##        
            if hypot(c_plr_x+25-bluep[0][0], c_plr_y+25-bluep[0][1]) < 45:
                cubepos = orangep[0]
                cube_switched= True
                cube_outways = orangep[-1] #direction it is facing
    ##            
            elif hypot(c_plr_x+25-orangep[0][0], c_plr_y+25-orangep[0][1]) < 45:
                cubepos = bluep[0]
                cube_switched= True
                cube_outways = bluep[-1]
    ##        
            if cube_switched:
                cube_last_tp = t.time()
                c_de_x = cube_begin_pos[0]- cube_startpos[0]
                c_de_y = cube_begin_pos[1] - cube_startpos[1]
    ##            
                cube_categories = {"Right":True, "Left":True, "Up": False, "Down": False}
                c_tele_adjust = {"Right": [50,-25], "Left": [-50,-25], "Up": [-25, -50], "Down": [-25, 50]}[cube_outways]
    ##
    ##            
                cubepos = [cubepos[0] + c_tele_adjust[0], cubepos[1] + c_tele_adjust[1]]
    ##            
                c_quadrant_adjust = {"Right": [abs, float], "Left": [rev_abs, float], "Up": [float, rev_abs], "Down": [float, abs]}[cube_outways] #adjusts where to teleport in quadrants
    ##
                if cube_categories[bluep[-1]] == cube_categories[orangep[-1]]: #Just changing one component
    ##                
    ##
                    if bluep[-1] == orangep[-1]: #Same one, inverse that component
    ##
                        c_ddx, c_ddy = c_quadrant_adjust[0](c_de_x), c_quadrant_adjust[1](c_de_y) #if on same wall got to make it push 180 the other portal
                        cube_forced_end = [ddx, ddy, 10]
    ##
                    else: #Opposite direction, keep it identical
                        cube_forced_end = [de_x, de_y, 10] #if opposite walls just change the playerpos, no quadrant changing needed
    ##                    
                else: #Changing both components
                    c_de_x, c_de_y = c_de_y, c_de_x #Reverse them
                    c_ddx, c_ddy = c_quadrant_adjust[0](c_de_x), c_quadrant_adjust[1](c_de_y) 
                    cube_forced_end = [c_ddx, c_ddy, 10]
    ##            
    ##            
    ####            if floatingmode == True:
    ####                if outways == "Right":
    ####                    playerpos[0] += 15
    ####                elif outways == "Left":
    ####                    playerpos[0] -= 15
        npos=cubepos[:]
    ##    #playerpos=collide(oldpos,newpos,map_grid)
    ##
        
        if jumpBlock(opos,npos,20,20):
            cube_state=state_change(state,True,keys[K_d],keys[K_a])
            grav_velocity2=-20 #a negative gravity makes it go up
    ##        
        if launch(opos,npos,20,20) == 'right':
            grav_velocity2 = -20
            c_xchange = -20
            cube_mode = 'launchingright'
    ##        
        if launch(opos,npos,20,20) == 'left':
            grav_velocity2 = -20
            c_xchange = -20
            cube_mode = 'launchingleft'
    ##        
        if cube_mode =='launchingright': #if nothing in forced_end
            cubepos=list(cubepos)
            cubepos[1] += grav_velocity2
            cubepos[0] -= c_xchange
            grav_velocity2+=0.75
            npos=cubepos[:]
            cubepos=collide(opos,npos,map_grid,floatingmode,20,20,20,20)
    ##        
        if cube_mode == 'launchingleft':
            cubepos=list(cubepos)
            cubepos[1] += grav_velocity2
            cubepos[0] += c_xchange
            grav_velocity2+=0.75
            npos=cubepos[:]
            cubepos=collide(opos,npos,map_grid,floatingmode,20,20,20,20) #VERY LAST LINE

            opos = cubepos[:]
            cube_begin_pos = cubepos[:]
            c_plr_x,c_plr_y = cubepos
            cube_switched = False
            if bluep[-1] and orangep[-1] and (t.time() - cube_last_tp>0.5 or abs(bluep[0][0]-orangep[0][0])<15) : #checks if there is a portal
                #switched = False
                cube_outways = None
        ##        
                if hypot(c_plr_x+25-bluep[0][0], c_plr_y+25-bluep[0][1]) < 45:
                    cubepos = orangep[0]
                    cube_switched= True
                    cube_outways = orangep[-1] #direction it is facing
        ##            
                elif hypot(c_plr_x+25-orangep[0][0], c_plr_y+25-orangep[0][1]) < 45:
                    cubepos = bluep[0]
                    cube_switched= True
                    cube_outways = bluep[-1]
        ##        
                if cube_switched:
                    cube_last_tp = t.time()
                    c_de_x = cube_begin_pos[0]- cube_startpos[0]
                    c_de_y = cube_begin_pos[1] - cube_startpos[1]
        ##            
                    cube_categories = {"Right":True, "Left":True, "Up": False, "Down": False}
                    c_tele_adjust = {"Right": [50,-25], "Left": [-50,-25], "Up": [-25, -50], "Down": [-25, 50]}[cube_outways]
        ##
        ##            
                    cubepos = [cubepos[0] + c_tele_adjust[0], cubepos[1] + c_tele_adjust[1]]
        ##            
                    c_quadrant_adjust = {"Right": [abs, float], "Left": [rev_abs, float], "Up": [float, rev_abs], "Down": [float, abs]}[cube_outways] #adjusts where to teleport in quadrants
        ##
                    if cube_categories[bluep[-1]] == cube_categories[orangep[-1]]: #Just changing one component
        ##                
        ##
                        if bluep[-1] == orangep[-1]: #Same one, inverse that component
        ##
                            c_ddx, c_ddy = c_quadrant_adjust[0](c_de_x), c_quadrant_adjust[1](c_de_y) #if on same wall got to make it push 180 the other portal
                            cube_forced_end = [ddx, ddy, 10]
        ##
                        else: #Opposite direction, keep it identical
                            cube_forced_end = [de_x, de_y, 10] #if opposite walls just change the playerpos, no quadrant changing needed
        ##                    
                    else: #Changing both components
                        c_de_x, c_de_y = c_de_y, c_de_x #Reverse them
                        c_ddx, c_ddy = c_quadrant_adjust[0](c_de_x), c_quadrant_adjust[1](c_de_y) 
                        cube_forced_end = [c_ddx, c_ddy, 10]
        ##            
        ##            
        ####            if floatingmode == True:
        ####                if outways == "Right":
        ####                    playerpos[0] += 15
        ####                elif outways == "Left":
        ####                    playerpos[0] -= 15
            npos=cubepos[:]
        ##    #playerpos=collide(oldpos,newpos,map_grid)
        ##

            if jumpBlock(opos,npos,20,20):
                cube_state=state_change(state,True,keys[K_d],keys[K_a])
                grav_velocity2=-20 #a negative gravity makes it go up
        ##        
            if launch(opos,npos,20,20) == 'right':
                grav_velocity2 = -20
                c_xchange = -20
                cube_mode = 'launchingright'
        ##        
            if launch(opos,npos,20,20) == 'left':
                grav_velocity2 = -20
                c_xchange = -20
                cube_mode = 'launchingleft'
        ##        
            if cube_mode =='launchingright': #if nothing in forced_end
                cubepos=list(cubepos)
                cubepos[1] += grav_velocity2
                cubepos[0] -= c_xchange
                grav_velocity2+=0.75
                npos=cubepos[:]
                cubepos=collide(opos,npos,map_grid,20,20,20,20)
        ##        
            if cube_mode == 'launchingleft':
                cubepos=list(cubepos)
                cubepos[1] += grav_velocity2
                cubepos[0] += c_xchange
                grav_velocity2+=0.75
                npos=cubepos[:]
                cubepos=collide(opos,npos,map_grid,20,20,20,20)
        
        return cubepos,cube_state,grav_velocity2,opos,cube_last_tp,cube_forced_end,cube_mode,c_xchange,cube_floatingmode,holding


    def holding_cube(dist,facing,holding,cubepos,playerpos):
        
        if dist<=63:
            if keys[K_e]:
                holding=True
                if keys[K_d]:
                    facing=0
                if keys[K_a]:
                    facing=1
                if facing==0:
                    cubepos[0]=playerpos[0]+43
                    cubepos[1]=playerpos[1]+9
                if facing==1:
                    cubepos[1]=playerpos[1]+9
                    cubepos[0]=playerpos[0]-13
                return holding,cubepos
        return holding,cubepos
    
    def move(playerpos,state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing,cubepos,holding):
        '''Moves the player, including jumping. Also accounts for velocity gained from gravity.
    Also includes the moving of player concerning portals.'''
         
        playerpos=list(playerpos)
        startpos = playerpos[:]
        holding=False
        holding,cubepos=holding_cube(hypot((playerpos[0]+6-cubepos[0]),(playerpos[1]-cubepos[1])),direction_face,holding,cubepos,playerpos)
        
        if keys[K_d] and not forced_end and mode != "launchingright" and mode != "launchingleft":
            playerpos=list(playerpos)
            prect=Rect(playerpos[0]+28,playerpos[1],11,60)
            crect=Rect(cubepos[0],cubepos[1],1,20)
            if prect.colliderect(crect):
                playerpos[0]+=2
                cubepos[0]+=2
            else:
                playerpos[0]+=5
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])

        if keys[K_a] and not forced_end and mode != "launchingright" and mode != "launchingleft":
            playerpos=list(playerpos)
            prect=Rect(playerpos[0]+9,playerpos[1],11,60)
            crect=Rect(cubepos[0]+19,cubepos[1],1,22)
            if prect.colliderect(crect):
                playerpos[0]-=2
                cubepos[0]-=2
            else:
                playerpos[0]-=5
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])

        newpos=playerpos[:]
        playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])
        oldpos = playerpos[:]
        
        if state=='jump' and not forced_end: #if nothing in forced_end
            playerpos=list(playerpos)
            playerpos[1]+=grav_velocity
            grav_velocity+=0.75
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])
            if playerpos==oldpos and oldpos[1]<newpos[1]: #this checks if player is coming down from jump//nothing is effecting  except gravity
                state, mode=state_change(state,False,False,False,mode)

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
        playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])

        oldpos = playerpos[:]
        
        begin_pos = playerpos[:]
        plr_x,plr_y = playerpos
        
        switched = False
        if bluep[-1] and orangep[-1] and (t.time() - last_tp>0.5 or abs(bluep[0][0]-orangep[0][0])<15) : #checks if there is a portal
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
                last_tp = t.time()
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

        if not switched and collide(oldpos,[oldpos[0],oldpos[1]+1],map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])==[oldpos[0],oldpos[1]+1] and state!='jump': #is gravity when player isn't jumping//checks if a pixel beneath is vacant or not
            state,mode=state_change(state,True,keys[K_d],keys[K_a],mode)
            grav_velocity=0
        if keys[K_w] and state!='jump':
            state,mode=state_change(state,True,keys[K_d],keys[K_a],mode)
            grav_velocity=-8 #a negative gravity makes it go up
            
        if jumpBlock(oldpos,newpos,pl,pw) and keys[K_w]:
            state,mode=state_change(state,True,keys[K_d],keys[K_a],mode)
            grav_velocity=-20 #a negative gravity makes it go up
            
        if launch(oldpos,newpos,pl,pw) == 'right':
            grav_velocity = -20
            xchange = -20
            mode = 'launchingright'
            
        if launch(oldpos,newpos,pl,pw) == 'left':
            grav_velocity = -20
            xchange = -20
            mode = 'launchingleft'
 #       print(mode)
        if mode =='launchingright': #if nothing in forced_end
            playerpos=list(playerpos)
            playerpos[1] += grav_velocity
            playerpos[0] -= xchange
            grav_velocity+=0.75
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])
            
        if mode == 'launchingleft':
            playerpos=list(playerpos)
            playerpos[1] += grav_velocity
            playerpos[0] += xchange
            grav_velocity+=0.75
            newpos=playerpos[:]
            playerpos=collide(oldpos,newpos,map_grid,floatingmode,pl,pw,cubepos[0],cubepos[1])
            
        return playerpos,state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing,cubepos,holding

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
    def collide(oldpos,newpos,grid,floatingmode,pl,pw,cx,cy):
        'Checks if the new position is vacant, if not, will return the old position'
        
        if pl!=20 and pw!=20:
            new_rect=Rect(newpos[0]+14,newpos[1],pl-29,pw)
            crect=Rect(cx,cy,20,20)
            
            if crect.colliderect(new_rect):
                return oldpos
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

    def jumpBlock(oldpos,newpos,pl,pw):
    
        if pl!=20:
            
            new_rect=Rect(newpos[0]+14,newpos[1],pl-29,pw+1)
        else:
            new_rect=Rect(newpos[0],newpos[1],pl,pw)
        for b in blockList:
            if b.colliderect(new_rect):
                return True
    def launch(oldpos,newpos,length,width):
        if length!=20:
            new_rect=Rect(newpos[0]+14,newpos[1],length-29,width+1)
        else:
            new_rect=Rect(newpos[0],newpos[1],length,width+1)
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
                
    def portal_rotation(pos):
        if facing(pos[0],pos[1])=='Up':
            return 0
        if facing(pos[0],pos[1])=='Down':
            return 180
        if facing(pos[0],pos[1])=='Right':
            return -90
        if facing(pos[0],pos[1])=='Left':
            return 90
    
    def shooting(bullet, col,hit,hit1):
         
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
            
        return portal,hit,hit1

    oldpos=[px,py]
    while running:
        b_click=False
        o_click=False
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        for e in event.get():
            if e.type==QUIT:
                operation = 'exit'
                running=False
            elif e.type==MOUSEBUTTONDOWN and e.button==1:
                b_click=True
            elif e.type==MOUSEBUTTONDOWN and e.button==3:
                o_click=True
            if keys[K_d]:
                direction_face=0
            if keys[K_a]:
                direction_face=1

        if levelindex == 0:
            screen.blit(level1,(0,0))
        elif levelindex == 1:
            screen.blit(level2,(0,0))
        elif levelindex == 2:
            screen.blit(level3,(0,0))
        elif levelindex == 3:
            screen.blit(level4,(0,0))
        elif levelindex == 4:
            screen.blit(level5,(0,0))

        

    #----MOVING----------------------------------
        
        (px,py),state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing,(cx,cy),holding=move([px,py],state,grav_velocity,oldpos,last_tp,forced_end,mode,xchange,floatingmode,face,changing,[cx,cy],holding)
    
        (cx,cy),cube_state,grav_velocity2,opos,cube_last_tp,cube_forced_end,cube_mode,c_xchange,cube_floatingmode,holding=cubemove([cx,cy],cube_state,grav_velocity2,opos,cube_last_tp,cube_forced_end,cube_mode,c_xchange,cube_floatingmode,holding)

    #----SHOOTING--------------------------------
        if b_click:
            bluep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]
        if (state=='idle' or state=='jump') and ((not keys[K_a] and not keys[K_d]) or (keys[K_a] and keys[K_d])):
            screen.blit(idle[direction_face],(px,py))
            
        
        bluep,hit,hit1 = shooting(bluep, (8,131,219),hit,hit1)
        
        if keys[K_r]:
            bluep=[None]
            orangep=[None]

        if o_click:
            orangep=[[px+25,py+25],atan2(my-(py+25), mx-(px+25)),1,None]

        orangep,hit,hit1 = shooting(orangep, (252,69,2),hit,hit1)
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
            ang=portal_rotation(bluep[0])
            screen.blit(transform.rotate(bluep_sprite[int(blue_frame)%3],ang),(bluep[0][0]-bluep_sprite[int(blue_frame)%3].get_width()//2,bluep[0][1]-bluep_sprite[int(blue_frame)%3].get_height()//2))

        if orangep[-1] != None and hit1:
            draw.circle(screen,(252,69,2),[int(e) for e in orangep[0]],8)
        screen.blit(cube,(cx,cy))
        frame+=1
        blue_frame+=0.3
        oldpos=[px,py]
        pRect = Rect(px,py,pl,pw)
     #   print(hypot(endpoint[0]-px,endpoint[1]-py))
        if hypot(endpoint[0]-px,endpoint[1]-py) < 90:
            levelindex += 1
            map_grid = loadMap(levels[levelindex])
            wall_rects,wall2_rects,blockList,launchPad,launchPad2,shield,mode,portal_state,state,hit,hit1,grav_velocity,xchange,forced_end,floatingmode,px,py = reset(wall_rects,wall2_rects,blockList,launchPad,launchPad2,shield,mode,portal_state,state,hit,hit1,grav_velocity,xchange,forced_end,floatingmode,px,py)
            t.sleep(0.5)
        display.flip()
    
    return operation
