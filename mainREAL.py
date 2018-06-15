#main
import menu  
import editTest  
import game  


running = True
main = menu.Main()
operation = 'intro'

while running:
    if operation == 'intro':
        operation = menu.Main()
    elif operation == 'exit':
        running = False
    elif operation == 'game':
        operation = game.Main()
quit()
