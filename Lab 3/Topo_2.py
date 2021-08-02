"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch

class Topo_2( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Hosts
        host_1 = self.addHost( 'h1' , mac = "00:00:00:00:00:01")
        host_2 = self.addHost( 'h2' , mac = "00:00:00:00:00:02")
        host_3 = self.addHost( 'h3' , mac = "00:00:00:00:00:03")
        host_4 = self.addHost( 'h4' , mac = "00:00:00:00:00:04")
        host_5 = self.addHost( 'h5' , mac = "00:00:00:00:00:05")    # este host es un servidor HTTP
        host_6 = self.addHost( 'h6' , mac = "00:00:00:00:00:06")    # este host es un servidor HTTP


        # Switches
        switch_1 = self.addSwitch( 's1' )
        switch_2 = self.addSwitch( 's2' )
        switch_3 = self.addSwitch( 's3' )
        switch_4 = self.addSwitch( 's4' )
        switch_5 = self.addSwitch( 's5' )

        # Links para switch_1
        self.addLink( switch_1, host_1, 1, 19)
        self.addLink( switch_1, host_2, 2, 20)
        self.addLink( switch_1, switch_2, 3, 9)
        self.addLink( switch_1, switch_3, 4, 10)
        self.addLink( switch_1, switch_5, 5, 18)

        # Links para switch_2
        self.addLink(switch_2, host_3, 6, 21)
        self.addLink(switch_2, host_4, 7, 22)
        self.addLink(switch_2, switch_4, 8, 13)

        # Links para switch_3
        self.addLink(switch_3, switch_4, 11, 14)
        self.addLink(switch_3, switch_5, 12, 17)


        # Links para switch_4
            # Todos repetidos

        # Links para switch_5
        self.addLink(switch_5, host_5, 15, 23)
        self.addLink(switch_5, host_6, 16, 24)









def runTopo():

    topo = Topo_2()

    # crear una red basada en la topologia, usando OVS y controlado remotamente.

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController (name, ip='127.0.0.1'),
        switch=OVSSwitch,
        autoSetMacs=True )

    # iniciar la red
    net.start()

    # Entregar un CLI para que puedan correr comandos
    CLI( net )

    # Cuando el usuario salga de la CLI, botar la red.
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info')
    runTopo()

topos = { 'anillo': ( lambda: Topo_2() ) }
