from pygame import *
screen=display.set_mode((800,600))
menu_background=image.load('menu_background.png')
sprint=[]
frame=0
for i in range(2,26):
    sprint.append(image.load(str(i+1)+'.png'))
def menu():
    global frame
    running = True
    myClock = time.Clock()
    
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return False

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(menu_background,(0,0))
        screen.blit(sprint[int(frame)%22],(400,300))
        frame+=0.3
        

                
        display.flip()
    quit()
    
running=True
while running:
    running=menu()
    

    display.flip()
quit()
