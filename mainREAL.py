#main
import menu  
import editTest  
import game  


running = True
operation = 'intro'

while running:
    if operation == 'intro':
        operation = menu.Main()
    elif operation == 'exit':
        running = False
    elif operation == 'game':
        operation = game.Main()
    elif operation == 'edit':
        operation = editTest.Main()
quit()

