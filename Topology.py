from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        # Add clients
        c1 = self.addHost('c1')
        c2 = self.addHost('c2')
        c3 = self.addHost('c3')
        dynDNS = self.addHost('dynDNS')
        cust = self.addHost('cust')
        control = self.addHost('control')
        proxy = self.addHost('proxy')
        cust_sw = self.addSwitch('s1')
        internet_sw = self.addSwitch('s2')
        mitigation_sw = self.addSwitch('s3')
        lan_sw = self.addSwitch('s4')
        # Add (bidirectional) links
        self.addLink(internet_sw, mitigation_sw)
        self.addLink(internet_sw, cust_sw)
        self.addLink(internet_sw, c1)
        self.addLink(internet_sw, c2)
        self.addLink(internet_sw, c3)
        self.addLink(cust_sw, cust)
        self.addLink(mitigation_sw, dynDNS)
        self.addLink(mitigation_sw, proxy)
        self.addLink(lan_sw, control)
        self.addLink(lan_sw, cust)
        self.addLink(lan_sw, dynDNS)
        self.addLink(lan_sw, proxy)
        


# Adding the 'topos' dict with a key/value pair to
# generate our newly defined topology enables one
# to pass in '--topo=mytopo' from the command line.
topos = {'mytopo': (lambda: MyTopo())}
