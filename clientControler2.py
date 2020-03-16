#!/usr/bin/python

from xaal.lib import Device, Engine, tools, Message
from xaal.tools import isalive
import sys, os


# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Menu 1
def play():
    print("Menu play !\n")
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'play',{})
    eng.start()	
    eng.process_tx_msg()
    exec_menu("9")
    return
 
 
# Menu 2
def pause():
    print("Menu pause !\n")
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'pause',{})
    eng.start()	
    eng.process_tx_msg()
    exec_menu("9")
    return

# Menu 3
def destinations():
    print("Menu destination !\n")
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'get_destinations',{})
    eng.start()	
    eng.process_tx_msg()
    msg = Message()
    while msg.is_reply() == False:
        msg = eng.receive_msg()
    #dest = msg.get_parameters()
    dest = msg.body
    dest2 = dest.split()
    print(dest2)
    #print("%s" % (msg.body))
    #exec_menu("9")
    return dest
 
# Menu 4
def sources():
    print("Menu source !\n")
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'get_sources',{})
    eng.start()	
    eng.process_tx_msg()
    msg = Message()
    while msg.is_reply() == False:
        msg = eng.receive_msg()
    src = msg.get_parameters()
    print(src)
    #exec_menu("9")
    return

# Back to main menu - Menu 9
def back():
    menu_actions['main_menu']()
 
# Exit program - Menu 0
def exit():
    sys.exit()

# Main definition - constants
menu_actions  = {}
addr = "f2fc6dac-4ffb-11ea-a473-0800276d39fa"
dev = Device("basic.basic", addr)
eng = Engine()
eng.add_device(dev)
addrMedia = ""
#### Choix du controler
devicesAlive = isalive.search(eng)
choiceDevice = input("Choisissez un device a controler (n°) >>  ")
os.system('clear')
#### Choix du renderer
list_dest = destinations()
print("ok")
choiceDest = input("Choisissez un renderer (n°) >>  ")
## test
#eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'set_destination("yo")',{})
#eng.start()
#eng.process_tx_msg()

def main():
    os.system('clear')
    
    print("Welcome,\n")
    
    print("Please choose the action (n°):")
    print("1. play")
    print("2. pause")
    print("3. destinations")
    print("4. sources")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)


# Menu definition
menu_actions = {
    'main_menu': main,
    '1': play,
    '2': pause,
    '3': destinations,
    '9': back,
    '0': exit,
}

if __name__ =='__main__':
    try:
        addr = None
        if len(sys.argv) > 1:
            addr = sys.argv[-1]
        main()
    except KeyboardInterrupt:
        pass
