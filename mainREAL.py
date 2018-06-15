#main
import menu  
import editTest  
import game  


running = True
main = menu.Main()
operation = 'intro'

while running:
    if operation == 'intro':
        menu.Main()
    if operation == 'exit':
        running = False
quit()
