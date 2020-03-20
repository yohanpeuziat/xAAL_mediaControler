#!/usr/bin/python

from xaal.lib import Device, Engine, tools, Message
from xaal.tools import isalive
import sys, os, time


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
    print("Liste des Renderer disponible\n")
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'get_destinations',{})
    eng.start()	
    eng.process_tx_msg()
    msg = Message()
    t0 = time.time()
    balise = True
    # Reçois le message suivant uniquement si le temps d'attente est inférieur à
    # 2 secondes et que la balise est à True
    while time.time() < (t0 + 2) and balise:
        msg = eng.receive_msg()
        # La balise passe à False si l'adresse source est égale à celle du
        # controler et que l'action est un get_destinations
        if msg.source == devicesAlive[int(choiceDevice)] and msg.action == 'get_destinations':
            balise = False
    dest = msg.body
    print(dest)
    ###### Voir pour réenvoyer le messge en cas d'échec de la réception
    #exec_menu("9")
    return dest
 
# Menu 4
def sources():
    print("Liste des Media disponible\n")
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'get_sources',{})
    eng.start()	
    eng.process_tx_msg()
    msg = Message()
    # Reçois le message suivant uniquement si l'adresse source est différente du
    # controler ou que l'action n'est pas un get_sources
    while msg.source != devicesAlive[int(choiceDevice)] or msg.action != 'get_sources':
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


# Main definition
addr = "f2fc6dac-4ffb-11ea-a473-0800276d39fa"
dev = Device("basic.basic", addr)
eng = Engine()
eng.add_device(dev)
addrMedia = ""

# Menu definition
menu_actions = {
    'main_menu': main,
    '1': play,
    '2': pause,
    '3': destinations,
    '9': back,
    '0': exit,
}

#### Choix du controler
devicesAlive = isalive.search(eng,"controlerMedia.basic")
choiceDevice = input("Choisissez un device a controler (n°) >>  ")
os.system('clear')
#### Choix du renderer
list_dest = destinations()
choiceDest = input("Choisissez un renderer (renderer : XXX) >>  ")
#### Mise en place du renderer
eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'set_destination',{'dest':choiceDest})
eng.start()
eng.process_tx_msg()
os.system('clear')
#### Choix du media
list_media = sources()
choiceMedia = input("Choisissez un media (media : XXX) >>  ")
#### Mise en place du media
eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'set_source',{'src':choiceMedia})
eng.start()
eng.process_tx_msg()


if __name__ =='__main__':
    try:
        addr = None
        if len(sys.argv) > 1:
            addr = sys.argv[-1]
        main()
    except KeyboardInterrupt:
        pass
