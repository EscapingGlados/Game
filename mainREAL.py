#main
import menu  
import editTest  
import game
import load


running = True
operation = 'intro'
levelName = ''

while running:
    if operation == 'intro':
        operation = menu.Main()
    elif operation == 'exit':
        running = False
    elif operation == 'game':
        operation = game.Main()
    elif operation == 'edit':
        operation = editTest.Main()
    elif operation == 'load':
        operation,levelName = load.Main()
quit()

