from pygame import *
from math import *
import time
import os
import pickle

init()

screen=display.set_mode((800,600))
running = True
player=[60,449,50,50]
cube=[500,459,40,40]
state='idle'
while running:
     
     keys=key.get_pressed()
     mb=mouse.get_pressed()
     mx,my=mouse.get_pos()
     for e in event.get():
          if e.type==QUIT:
               running=False
               
     if keys[K_d]:
          if not Rect(player).colliderect(Rect(cube)):
               player[0]+=5
          else:
               player[0]+=1
               cube[0]+=1
          state='left'
     if keys[K_a]:
          player[0]-=5
          state='right'
     if not keys[K_a] and not keys[K_d]:
          state='idle'
     draw.rect(screen,(255,255,255),(0,0,800,600))
     draw.rect(screen,(0,200,20),(0,500,800,100))
     draw.rect(screen,(0,0,255),Rect(player))
     draw.rect(screen,(255,0,0),Rect(cube))
     print(state)

     display.flip()
quit()
     
