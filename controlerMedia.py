
from xaal.lib import Device,Engine,tools
from xaal.tools import isalive
import sys

def main(addr):
    if addr == None:
        addr = tools.get_random_uuid()
    dev = Device("controlerMedia.basic",addr)
    dev.product_id = 'Controler DLNA'
    dev.url = 'http://www.acme.org'
        
    # attributes
    destination_media = dev.new_attribute('destination_media')
    source_media = dev.new_attribute('source_media')
    state_media = dev.new_attribute('state_media')
    position_media = dev.new_attribute('position_media')

    dev.dump()
    
    # methods
    def get_attributes():
        print("Attributs")


    ########### Ensemble des methodes liees a la mise en place du media ##########
    def set_destination(_dest):
	# Met la valeur du media player a utiliser dans la variable "destination_media"
        destination_media.value = _dest
        print("Destination \"" + _dest + "\" is set")

    def get_destinations():
	# Interroge le dBus pour connaitre les media renderer en DLNA
	# Envoie à l'utilisateur les destinations sous forme de liste
        available_dest = {"renderer1":"salon", "renderer2":"cuisine"}
        print("Display destinations")
        return available_dest

    def set_source(_src):
	# Met la valeur du media server a utiliser dans la variable "source_media"
        source_media.value = _src
        print("Source \"" + _src + "\" is set")

    def get_sources():
	# Interroge le dBus pour connaitre les media server en DLNA
	# Envoie à l'utilisateur les medias sous forme de liste
        available_media = {"media1":"NAS\\video1", "media2":"NAS\\video2"}
        print("Display sources")
        return available_media


    ########## Ensemble des methodes liees a l'etat du media lorsqu'il est en cours de lecture #########
    def play():
        state_media.value = True
        # Commande DLNA pour lancer le media
        print("%s Play" % dev)
    
    def pause():
        state_media.value = False
        # Commande DLNA pour mettre le media sur pause
        print("%s Pause" % dev)

    def stop():
        print("Media is stop")

    def next():
        print("Next media is play")

    def prev():
        print("Previous media is play")

    def moving_forward():
        print("Media is forwarding of 10 secondes")

    def moving_back():
        print("Media is backing of 10 secondes")
    
    dev.add_method('get_attributes',get_attributes)
    dev.add_method('set_destination',set_destination)
    dev.add_method('get_destinations',get_destinations)
    dev.add_method('set_source',set_source)
    dev.add_method('get_sources',get_sources)   
    dev.add_method('play',play)
    dev.add_method('pause',pause)
    dev.add_method('stop',stop)
    dev.add_method('next',next)
    dev.add_method('prev',prev)
    dev.add_method('moving_forward',moving_forward)
    dev.add_method('moving_back',moving_back)

    eng = Engine()
    eng.add_device(dev)
    eng.run()


if __name__ =='__main__':
    try:
        addr = None
        if len(sys.argv) > 1:
            addr = sys.argv[-1]
        main(addr)
    except KeyboardInterrupt:
        pass
