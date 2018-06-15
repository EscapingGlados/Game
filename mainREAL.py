#mainReal.py
#Aaryan & Feeda
#2D portal game. It's like a platformer with portals

import menu  
import editTest  
import game
import load
import testingLevel
import loadTest

running = True
operation = 'intro'
levelName = ''
startingLevel = ''

while running:
    if operation == 'intro':
        operation = menu.Main()
        
    elif operation == 'exit':
        running = False
        
    elif operation == 'game':
        operation = game.Main()
        
    elif operation == 'edit':
        
        operation = editTest.Main(levelName)
        
    elif operation == 'load':
        operation,levelName = load.Main()
        
    elif operation == 'loadTest':
        operation,startingLevel = loadTest.Main()
        
    elif operation == 'testingLevel':
        
        operation = testingLevel.Main(startingLevel)
        
quit()

