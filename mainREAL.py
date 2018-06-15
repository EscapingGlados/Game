#main
import menu  
import editTest  
import game
import load
import testingLevel
import loadTest

#ESCAPING GLADOS
#BY AARYAN PATEL AND FEEDA ELAHRESH
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
        print("3")
        operation = editTest.Main(levelName)
        
    elif operation == 'load':
        operation,levelName = load.Main()
        
    elif operation == 'loadTest':
        operation,startingLevel = loadTest.Main()
        
    elif operation == 'testingLevel':
        print("2")
        operation = testingLevel.Main(startingLevel)
        
quit()

