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

# Permet de recevoir les destinations
def destinations():
    global compteur_attente_dest
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
        # Permet de ne pas traiter les messages None qui font planter le programme
        if msg != None:
            # La balise passe à False si l'adresse source est égale à celle du
            # controler et que l'action est un get_destinations
            if msg.source == devicesAlive[int(choiceDevice)] and msg.action == 'get_destinations':
                balise = False
    # variable globale qui permet de relancer un maximum de 5 fois la commande get_destinations en cas de non reception de réponse
    # Pour tester cette fonction, mettre le return de la fonction (dans le fichier controlerMedia.py) en commentaire
    if compteur_attente_dest < 5:
        # Sortie de la boucle à cause du temps : appelle de la fonction a nouveau
        if balise:
            print("Pas de reception dest")
            compteur_attente_dest += 1
            dest = destinations()
        # Sortie de la boucle à cause de la balise : affichage du résultat
        else:
            dest = msg.body
            print("Liste des Renderer disponible\n")
            print(dest)
            print("\n")
    else:
        print("Désolé pas de renderer disponible")
        return "Error"
    #exec_menu("9")
    return dest
 
# Permet de recevoir les sources
def sources():
    global compteur_attente_src
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'get_sources',{})
    eng.start()	
    eng.process_tx_msg()
    msg = Message()
    t0 = time.time()
    balise = True
    # Reçois le message suivant uniquement si le temps d'attente est inférieur à
    # 2 secondes et que la balise est à True
    while time.time() < (t0 + 2) and balise:
        msg = eng.receive_msg()
        # Permet de ne pas traiter les messages None qui font planter le programme
        if msg != None:
            # La balise passe à False si l'adresse source est égale à celle du
            # controler et que l'action est un get_sources
            if msg.source == devicesAlive[int(choiceDevice)] and msg.action == 'get_sources':
                balise = False
    # variable globale qui permet de relancer un maximum de 5 fois la commande get_sources en cas de non reception de réponse
    # Pour tester cette fonction, mettre le return de la fonction (dans le fichier controlerMedia.py) en commentaire
    if compteur_attente_src < 5:
        # Sortie de la boucle à cause du temps : appelle de la fonction a nouveau
        if balise:
            print("Pas de reception src")
            compteur_attente_src += 1
            src = sources()
        # Sortie de la boucle à cause de la balise : affichage du résultat
        else:
            src = msg.body
            print("Liste des Sources disponible\n")
            print(src)
            print("\n")
    else:
        print("Désolé pas de Sources disponible")
        return "Error"
    #exec_menu("9")
    return src

# Saisir une nouvelle destination - Menu 3
def set_destination():
    #### Choix du renderer
    list_dest = destinations()
    if list_dest == "Error":
        exit()
    choiceDest = input("Choisissez un renderer (renderer : XXX) >>  ")
    #### Mise en place du renderer
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'set_destination',{'dest':choiceDest})
    eng.start()
    eng.process_tx_msg()
    exec_menu("9")
    return

# Saisir une nouvelle source - Menu 4
def set_source():
    #### Choix du media
    list_media = sources()
    if list_media == "Error":
        exit()
    choiceMedia = input("Choisissez un media (media : XXX) >>  ")
    #### Mise en place du media
    eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'set_source',{'src':choiceMedia})
    eng.start()
    eng.process_tx_msg()
    exec_menu("9")
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
    print("3. destination")
    print("4. source")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)


# Main definition
addr = "f2fc6dac-4ffb-11ea-a473-0800276d39fa"
dev = Device("basic.basic", addr)
eng = Engine()
eng.add_device(dev)
addrMedia = ""
compteur_attente_dest = 0
compteur_attente_src = 0

# Menu definition
menu_actions = {
    'main_menu': main,
    '1': play,
    '2': pause,
    '3': set_destination,
    '4': set_source,
    '9': back,
    '0': exit,
}

#### Choix du controler
devicesAlive = isalive.search(eng,"controlerMedia.basic")
choiceDevice = input("Choisissez un device a controler (n°) >>  ")
os.system('clear')
#### Choix du renderer
list_dest = destinations()
if list_dest == "Error":
    exit()
choiceDest = input("Choisissez un renderer (renderer : XXX) >>  ")
#### Mise en place du renderer
eng.send_request(dev,[devicesAlive[int(choiceDevice)]],'set_destination',{'dest':choiceDest})
eng.start()
eng.process_tx_msg()
os.system('clear')
#### Choix du media
list_media = sources()
if list_media == "Error":
    exit()
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
