from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink, Intf
from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
        # Add clients
        c1 = net.addHost('c1', ip="10.0.1.2/24")
        c2 = net.addHost('c2', ip="10.0.1.3/24")
        c3 = net.addHost('c3', ip="10.0.1.4/24")
        cust = net.addHost('cust', ip="10.0.2.2/24")
        dynDNS = net.addHost('dynDNS', ip="192.168.1.3/24")
        proxy = net.addHost('proxy', ip="192.168.1.2/24")
        control = net.addHost('control', ip="192.168.1.4/24")
        s1 = net.addSwitch('s1')
        s2 = net.addSwitch('s2')
        s3 = net.addSwitch('s3')
        r1 = net.addHost('r1')
        r2 = net.addHost('r2')
        c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )


        # Add (bidirectional) links
        #intenet network
        net.addLink(s1, c1) 
        net.addLink(s1, c2)
        net.addLink(s1, c3)
        net.addLink(s1, r1)

        #customer network
        net.addLink(s2, cust)
        net.addLink(s2, r1)

        #Backbone
        net.addLink(r1, r2)

        #IronDome Network
        net.addLink(s3, proxy)
        net.addLink(s3, dynDNS)
        net.addLink(s3, control)
        net.addLink(s3, r2)

        net.build()
        c0.start()
        s1.start( [c0] )
        s2.start( [c0] )
        s3.start( [c0] )

        # Router 1 config
        r1.cmd("ifconfig r1-eth0 0")
        r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:20:01")
        r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-eth0")
        r1.cmd("ifconfig r1-eth1 0")
        r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:20:02")
        r1.cmd("ip addr add 10.0.2.1/24 brd + dev r1-eth1")
        r1.cmd("ifconfig r1-eth2 0")
        r1.cmd("ifconfig r1-eth2 hw ether 00:00:00:00:20:03")
        r1.cmd("ip addr add 10.0.3.1/24 brd + dev r1-eth2")
        r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

	    # Router 2 config
        r2.cmd("ifconfig r2-eth0 0")
        r2.cmd("ifconfig r2-eth0 hw ether 00:00:00:00:30:01")
        r2.cmd("ip addr add 10.0.3.2/24 brd + dev r2-eth0")
        r2.cmd("ifconfig r2-eth1 0")
        r2.cmd("ifconfig r2-eth1 hw ether 00:00:00:00:30:02")
        r2.cmd("ip addr add 192.168.1.1/24 brd + dev r2-eth1")
        r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

	    # Static routes
        r1.cmd("ip route add default via 10.0.3.2")
        r2.cmd("ip route add default via 10.0.3.1")
        c1.cmd("ip route add default via 10.0.1.1")
        c2.cmd("ip route add default via 10.0.1.1")
        c3.cmd("ip route add default via 10.0.1.1")
        cust.cmd("ip route add default via 10.0.2.1")
        dynDNS.cmd("ip route add default via 192.168.1.1")
        proxy.cmd("ip route add default via 192.168.1.1")
        control.cmd("ip route add default via 192.168.1.1")
        # Influx deamon start
        control.cmd("influxd &")

        # *** Router 2 NAT ***
        # - Proxy configuration
        r2.cmd("iptables -t nat -A PREROUTING -p tcp -d 10.0.3.2 --dport 80 -i r2-eth0 -j DNAT --to-destination 192.168.1.2")
        r2.cmd("iptables -t nat -A POSTROUTING -p tcp -s 192.168.1.2 -i r2-eth1 -j SNAT --to 10.0.3.2")
	
        # - DNS configuration
        # -- HTTP Service
        r2.cmd("iptables -t nat -A PREROUTING -p tcp -d 10.0.3.2 --dport 8000 -i r2-eth0 -j DNAT --to-destination 192.168.1.3")
        r2.cmd("iptables -t nat -A POSTROUTING -p tcp -s 192.168.1.3 -i r2-eth1 -j SNAT --to 10.0.3.2")
        
        # -- DNS Service
        r2.cmd("iptables -t nat -A PREROUTING -p udp -d 10.0.3.2 --dport 53 -i r2-eth0 -j DNAT --to-destination 192.168.1.3")
        r2.cmd("iptables -t nat -A POSTROUTING -p udp -s 192.168.1.3 -i r2-eth1 -j SNAT --to 10.0.3.2")
        
        # *** DNS configuration *** NOT WORKING AUTOMATICALLY
        # - Start DNS
        dynDNS.cmd("cd dns && ruby dns.rb &")
        
        # - Change default DNS
        r1.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        r2.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        c1.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        c2.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        c3.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        cust.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        dynDNS.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        proxy.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
        control.cmd('echo "nameserver 10.0.3.2" >> /etc/resolv.conf')
	
        CLI( net )
        
        # *** Customer Webserver *** NOT WORKING AUTOMATICALLY
        cust.cmd("python -m http.server --directory customer_webserver/ 80")

        # *** Command and Controll *** 
        s4 = net.addSwitch('s4')
        net.addLink(s3, control)
        s4_node = mn.getNodeByName("s4")
        Intf("lo", node=s4_node)
    	
        CLI(mn)

        

# Adding the 'topos' dict with a key/value pair to
# generate our newly defined topology enables one
# to pass in '--topo=mytopo' from the command line.
topos = {'mytopo': (lambda: MyTopo())}
