# Init SW
curl -X PUT http://localhost:8080/firewall/module/enable/all

ip link add name s2-script type dummy
ip link set s2-script up
ovs-vsctl add-port s2 s2-script
ovs-ofctl show s2


# Clients to customer
## SW1
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000001

# SW2
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000002
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000002
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000002

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000002
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000002
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000002


# Clients to IronDome
## SW1
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000001

## SW3
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000003

# IronDome (internal) to Internet (R2)
## SW3
curl -X POST -d '{"nw_src": "192.168.1.1/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.1/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.1/32", "nw_dst": "192.168.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "192.168.1.1/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "192.168.1.1/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.4/32", "nw_dst": "192.168.1.1/32"}' http://localhost:8080/firewall/rules/0000000000000003

# IronDome to customer
##SW3
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000003

##SW2
curl -X POST -d '{"nw_src": "10.0.3.2/32", "nw_dst": "10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000002
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst": "10.0.3.2/32"}' http://localhost:8080/firewall/rules/0000000000000002

## Clients to IronDome (internal)
## DNS
### SW1
curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000001
#
curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001

# SW3
curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.3/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "192.168.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003

# PROXY
## SW1
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000001

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000001

# SW3
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "10.0.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "10.0.1.3/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst": "10.0.1.4/32"}' http://localhost:8080/firewall/rules/0000000000000003

curl -X POST -d '{"nw_src": "10.0.1.2/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.1.3/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.1.4/32", "nw_dst": "192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003

# CC to DNS
## SW3
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst":"10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000003
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst":"192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000003

## SW2
curl -X POST -d '{"nw_src": "192.168.1.2/32", "nw_dst":"10.0.2.2/32"}' http://localhost:8080/firewall/rules/0000000000000002
curl -X POST -d '{"nw_src": "10.0.2.2/32", "nw_dst":"192.168.1.2/32"}' http://localhost:8080/firewall/rules/0000000000000002
