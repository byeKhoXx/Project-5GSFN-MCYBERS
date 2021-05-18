from datetime import date
import json
import schedule
import threading
import time
import sys
from DB import clients_managment
import os
import requests

# Params of client
inp = input("Client:")

client = clients_managment.get_client_by_name(inp)

while client is None:
    print("This client doesn't exist")
    inp = input("Client:")
    client = clients_managment.get_client_by_name(inp)

# Client's data
DYNDNS_Name = '' # Name from client in DynDNS
DYNDNS_Pass = '' # Pass from client in DynDNS
DynDNS_IP = '' # IP from the DynDNS
REVERSE_Proxy_IP = '' # Reverse proxy IP
SwitchID = '' # Switch ID of the customer
VlanID = '' # VLAN ID

# Protection state
DoSactive = False
DDoSactive = False

'''
INIT TEST ZONE
'''

packets = clients_managment.get_number_15_minutes(client)
print(packets)

#mean10 = clients_managment.get_mean_for_last(client, time_slot_calc)
#print(mean10)

packets1 = clients_managment.get_last_two_minutes(client)
print(packets1)

'''
END TEST ZONE
'''

# cron ->sched.scheduler  https://docs.python.org/3/library/sched.html
# DynDNS: https://github.com/arkanis/minidyndns

def last_minute(packet):
    # TODO -> Check if packet timestap is from last minute
    now = time.time()
    ptime = packet.timestamp


# TODO ->crida que ha de fer el Reverseproxy quan no hi hagi sintomes de DDoS
def endDDoS():
    global DYNDNS_Name
    global DYNDNS_Pass
    global DynDNS_IP
    global client
    # Change DynDNS record
    r = requests.get('http://'+ DynDNS_IP + '/?myip='+ client.ip, auth=(DYNDNS_Name, DYNDNS_Pass))
    print(r)

# Every 10min we check if DoS is active
def checkDoS():
    global DoSactive
    global SwitchID
    global VlanID
    # If DoS is active we dissable the protection
    if DoSactive == True:
        DoSactive = False
        # Delete rules
        r = requests.delete('http://localhost:8080/firewall/rules/' + SwitchID + '/' + VlanID, data={'rule_id': 'all'})
        print(r)
        

def dos_attack_handler(key):
    print("DoS handler")

    global DoSactive
    global SwitchID
    global VlanID
    # DoS protection active
    DoSactive = True
    # Add rule to block the IP
    r = requests.post('http://localhost:8080/firewall/rules/' + SwitchID + '/' + VlanID, data={'nw_src':key, 'actions': 'DENY', 'priority': '2'})
    print(r)

def ddos_attack_handler():
    print("DDoS handler")

    global DDoSactive
    global DYNDNS_Name
    global DYNDNS_Pass
    global DynDNS_IP
    global REVERSE_Proxy_IP
    global SwitchID
    global VlanID
    # DDoS protection active
    DDoSactive = True
    # Change DynDNS record
    r = requests.get('http://'+ DynDNS_IP + '/?myip='+REVERSE_Proxy_IP, auth=(DYNDNS_Name, DYNDNS_Pass))
    print(r)
    # TODO -> Call a reverse proxy
    # Firewall block trafic
    r = requests.post('http://localhost:8080/firewall/rules/' + SwitchID + '/' + VlanID, data={'actions': 'DENY', 'priority': '2'})
    print(r)

# DoS detection
def DoS():
    print("Checking for DoS")
    global client
    # Get the flows of last two minutes
    packets = clients_managment.get_last_two_minutes(client)

    seconds = time.time()
    r = int((seconds / 60) % 2)

    d1 = dict()  # Packets from last minute [ip_src, number of packets]
    d2 = dict()  # Packets from last two minutes  [ip_src, number of packets]

    for packk in packets:
        # Check if the packet is from last minute
        if(last_minute(packk)):
            # Count packets from last minute
            if (packk["ip_src"] in d1):
                d1[packk["ip_src"]] = d1[packk["ip_src"]] + 1
            else:
                d1[packk["ip_src"]] = 1
        # Count packets from last two minutes
        if (packk["ip_src"] in d2):
            d2[packk["ip_src"]] = d1[packk["ip_src"]] + 1
        else:
            d2[packk["ip_src"]] = 1


    # Check last minute
    for key in d1:
        print("D1-> " + str(d1[key]))
        if d1[key] > 20:
            # Attack using ip = key
            print("NEW ATTACK: DoS")
            dos_attack_handler(key)
    d1 = dict()
    # Check last two minutes
    for key in d2:
        print("D2-> " + str(d2[key]))
        if d2[key] > 20:
            # Attack using ip = key
            print("NEW ATTACK: DoS")
            dos_attack_handler(key)
    d2 = dict()


# DDoS detection
def DDoS():
    print("Checking for DDoS")
    # Calculate the time slot
    time_slot_calc = int((time.localtime().tm_hour * 60 + time.localtime().tm_min) / 15)  # Every 10 min
    global client
    # Get the last 15 min traffic
    packets = clients_managment.get_number_15_minutes(client)
    # Get the mean
    mean10 = clients_managment.get_mean_for_last(client, time_slot_calc)
    if packets > mean10 * 2:
        # DDoS attack
        print("NEW ATTACK: DDoS")
        ddos_attack_handler("")


def scheduler():  # Scheduler for tasks every X minutes
    schedule.every().minute.do(DoS)  # Executing "Dos()" every minute
    schedule.every(10).minutes.do(checkDoS)  # Executing "checkDoS()" every 10 minute
    schedule.every(15).minutes.do(DDoS)  # Executing "DDoS()" eevry 15 minutes
    while 1:
        schedule.run_pending()


t = threading.Thread(target=scheduler)  # Threading the scheduler
# t.daemon = True  # set thread to daemon ('ALGO' won't be printed in this case)
t.start()