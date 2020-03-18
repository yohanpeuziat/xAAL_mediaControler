
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
	# destination_media.value = ...
        print("Destination is set : " + _dest)

    def get_destinations():
	# Interroge le dBus pour connaitre les media renderer en DLNA
	# Envoie à l'utilisateur les destinations sous forme de liste
        available_dest = {"rain":"rainning", "rend":"renderer"}
        print("Display destinations")
        return available_dest

    def set_source():
	# Met la valeur du media server a utiliser dans la variable "source_media"
        print("Source is set")

    def get_sources():
	# Interroge le dBus pour connaitre les media server en DLNA
	# Stock le résultat dans la variable "available_source" qui est sous forme de 		list
        print("Display sources")


    ########## Ensemble des methodes liees a l'etat du media lorsqu'il est en cours de lecture #########
    def play():
        state_media.value = True
        print("%s Play" % dev)
    
    def pause():
        state_media.value = False
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
