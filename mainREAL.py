#mainReal.py
#Aaryan & Feeda
#2D portal game. It's like a platformer with portals

##############################Features####################################################
#Portal gun can teleport player
#Vector is maintained (force into portal can translate into whatever direction)
#Pretty loading screen with moving sprites
#Level Editor - Allows back-end workers to work on collisions of levels easier
#User Level Editor - Allows user to play around in his/her own sandbox creative mode
#Lets user save and load any 'levels' they created
#Various blocks do different things (launchpad, left o 



import menu  #imports our main menu file
import editTest  #imports our editor for user's levels
import game #imports games
import load #imports our file that loads in saved pickle files user created to edit
import testingLevel #imports file so user can test out level they created
import loadTest #loads in pickle file the user created

running = True
operation = 'intro' #operation is tracking what is happening in the game,default is intro
levelName = '' #getting the name of the level from load
startingLevel = '' #getting the name of the level from loadTest

while running:
    if operation == 'intro': #while the operation is 'intro', the menu script runs
        operation = menu.Main()
        
    elif operation == 'exit': #if user tries quitting operation turns into 'exit', closing everything
        running = False
        
    elif operation == 'game':#if user clicks start, actual game runs
        operation = game.Main()
        
    elif operation == 'edit': #editing script
        operation = editTest.Main(levelName)
        
    elif operation == 'load': #load script
        operation,levelName = load.Main()
        
    elif operation == 'loadTest': #loadTest script
        operation,startingLevel = loadTest.Main()
        
    elif operation == 'testingLevel': #testingLevel script
        operation = testingLevel.Main(startingLevel)
    
quit()

