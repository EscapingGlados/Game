from menu import *
from pygame import *
screen=display.set_mode((800,600))
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
running=True
while running:
    running=menu()
    display.flip()
quit()
