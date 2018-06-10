import pygame

pygame.init()

size=[500,500]
screen = pygame.display.set_mode(size)
running = True

grid = open("cmask.txt").read().strip().split("\n")
walls=[]
buttons={}

for n in range(len(grid)):
  for i in range(len(grid[n])):
    if grid[n][i] =="w":
      walls.append(pygame.Rect(i*100,n*100,100,100))
    if grid[n][i].isdigit() and grid[n][i]!="0":
      walls.append(pygame.Rect(i*100,n*100,100,100))
      if grid[n][i] not in buttons:
        buttons[grid[n][i]]=[]
      buttons[grid[n][i]].append(pygame.Rect(i*100,n*100,100,100))
      
state = "idle"
gravityVelocity = 0
lengthL,lengthW=[35,35]
pPosition = [100,400-lengthW]
player = pygame.draw.rect(screen,(50,50,182),(pPosition[0],pPosition[1],lengthL,lengthW))

movingwalls={"1":[pygame.Rect(310,150,80,20),False],"2":[pygame.Rect(110,150,80,20),False]}
movingWG = [[150,350],[350,150]]#max x/y, min x/y

directionRelation = {"down":["top",[0,1],[0,-1]],"right":["right",[1,0],[-1,0]],"left":["left",[-1,0],[1,0]],"up":["top",[0,-1],[0,1]]}
direction = ["down","up"]
def drawBackground(screen):
  pygame.draw.rect(screen,(122,50,50),(0,0,500,500))
  pygame.draw.rect(screen,(255,255,255),(100,100,300,300))
  pygame.draw.rect(screen,(122,50,50),(200,200,100,100))
  
def move(playerPos):
  global state
  global gravityVelocity
  keys=pygame.key.get_pressed()
  oldPos = playerPos[:]

  if keys[pygame.K_RIGHT]:
    playerPos[0]+=1
    newPos=playerPos[:]
    playerPos = collide(oldPos,newPos,grid)
    
  if keys[pygame.K_LEFT]:
    playerPos[0]-=1
    newPos=playerPos[:]
    playerPos = collide(oldPos,newPos,grid)
  oldPos = playerPos[:]
  if collide(oldPos,[oldPos[0],oldPos[1]+4],grid)==[oldPos[0],oldPos[1]+4] and state!="jump":
    state="jump"
    gravityVelocity=0
  if keys[pygame.K_UP] and state!="jump":
    state="jump"
    gravityVelocity=-8
  if state =="jump":
    playerPos[1]+=gravityVelocity
    gravityVelocity+=0.1
    newPos=playerPos[:]
    playerPos = collide(oldPos,newPos,grid)
    if playerPos==oldPos and oldPos[1]<newPos[1]:
      state="idle"
    if playerPos==oldPos and oldPos[1]>newPos[1]:
      gravityVelocity =0
      
      
  return playerPos

def collide(oldpos,newpos,grid):
  global buttons, movingwalls,colliding
  newRect = pygame.Rect(newpos[0],newpos[1],lengthL,lengthW)
  otherRect = pygame.Rect(newpos[0],newpos[1]+1,lengthL,lengthW)
  colliding=False
  for key,bRectList in buttons.items():
    for bRect in bRectList:
      pygame.draw.rect(screen,(0,255,0),otherRect,1)
      pygame.draw.rect(screen,(0,255,0),bRect,1)
      if bRect.colliderect(otherRect):
        movingwalls[key][-1]=True
  for wRect in walls:
    if wRect.colliderect(newRect):
      if wRect.top<newRect.top:
        colliding=True

      return oldpos
  for mRect in list(movingwalls.values()):
    if mRect[0].colliderect(newRect):

      return oldpos    
  return newpos

def moveWall(ppos):
  global movingwalls

  newRect = pygame.Rect(ppos[0],ppos[1],lengthL,lengthW)
  for key,mRectList in movingwalls.items():
    goldenIndex = int(key)-1
    bound, change1,change2 = directionRelation[direction[goldenIndex]]
    rectSides={"right": mRectList[0].right,"left":mRectList[0].left,"bottom":mRectList[0].bottom,"top":mRectList[0].top}
    
    if direction[goldenIndex] == "down" or direction[goldenIndex] == "right":
      if mRectList[-1] and rectSides[bound]<movingWG[int(key)-1][1]:
        xRect, yRect, wRect, hRect = mRectList[0]
        movingwalls[key]=[pygame.Rect(xRect + change1[0], yRect + change1[1], wRect, hRect),True]
      elif mRectList[-1]==False and rectSides[bound]>movingWG[int(key)-1][0] and not colliding:
        xRect, yRect, wRect, hRect = mRectList[0]
        movingwalls[key]=[pygame.Rect(xRect + change2[0], yRect + change2[1], wRect, hRect),False]
        if mRectList[0].colliderect(newRect):
          ppos[1]=mRectList[0].top-lengthW
    else:
      if mRectList[-1] and rectSides[bound]>movingWG[int(key)-1][1]:
        xRect, yRect, wRect, hRect = mRectList[0]
        movingwalls[key]=[pygame.Rect(xRect + change1[0], yRect + change1[1], wRect, hRect),True]
      elif mRectList[-1]==False and rectSides[bound]<movingWG[int(key)-1][0] and not colliding:
        xRect, yRect, wRect, hRect = mRectList[0]
        movingwalls[key]=[pygame.Rect(xRect + change2[0], yRect + change2[1], wRect, hRect),False]
        if mRectList[0].colliderect(newRect):
          ppos[1]=mRectList[0].top-lengthW
  return ppos
c=0
while running:
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      running = False
  for key in movingwalls:
    movingwalls[key][-1]=False


  drawBackground(screen)
  pPosition = move(pPosition)
  pPosition = moveWall(pPosition)
  player = pygame.draw.rect(screen,(50,50,182),(pPosition[0],pPosition[1],lengthL,lengthW))
  for key,mRectList in movingwalls.items():
    pygame.draw.rect(screen,(0,255,0),mRectList[0])
  pygame.time.wait(5)
  pygame.display.flip()
quit()











