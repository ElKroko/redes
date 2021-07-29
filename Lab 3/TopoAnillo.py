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

class TopoAnillo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Hosts
        host_1 = self.addHost( 'h1' , mac = "00:00:00:00:00:01")
        host_2 = self.addHost( 'h2' , mac = "00:00:00:00:00:02")
        host_3 = self.addHost( 'h3' , mac = "00:00:00:00:00:03")
        host_4 = self.addHost( 'h4' , mac = "00:00:00:00:00:04")
        host_5 = self.addHost( 'h5' , mac = "00:00:00:00:00:05")
        host_6 = self.addHost( 'h6' , mac = "00:00:00:00:00:06")
        host_7 = self.addHost( 'h7' , mac = "00:00:00:00:00:07")
        host_8 = self.addHost( 'h8' , mac = "00:00:00:00:00:08")

        # Switches
        switch_1 = self.addSwitch( 's1' )
        switch_2 = self.addSwitch( 's2' )
        switch_3 = self.addSwitch( 's3' )
        switch_4 = self.addSwitch( 's4' )

        # Links para switch_1
        self.addLink( host_1, switch_1, 17, 1)
        self.addLink( host_2, switch_1, 18, 2)

        # Links para switch_2
        self.addLink( host_3, switch_2, 19, 5)
        self.addLink( host_4, switch_2, 20, 6)

        # Links para switch_1
        self.addLink( host_5, switch_3, 21, 9)
        self.addLink( host_6, switch_3, 22, 10)

        # Links para switch_1
        self.addLink( host_7, switch_4, 23, 13)
        self.addLink( host_8, switch_4, 24, 14)

        # Links entre switches
        self.addLink( switch_1, switch_2, 3, 7)
        self.addLink( switch_1, switch_4, 4, 15)
        self.addLink( switch_2, switch_3, 8 , 11)
        self.addLink( switch_3, switch_4, 12, 16)


def runTopo():

    topo = topoAnillo()

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

topos = { 'anillo': ( lambda: TopoAnillo() ) }
