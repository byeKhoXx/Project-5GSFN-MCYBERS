from datetime import date
import json
import schedule
import threading
import time
import clients_managment
import os
import requests

# Params of client
inp = input("Client:")

client = clients_managment.get_client_by_name(inp)
# TODO -> Dades clients
DYNDNS_NAME = ''
DYNDNS_PASS = ''
DYNDNS_IP = ''
REVERSE_PROXY_IP = ''
SwitchID = ''
VLANID = ''

# Protection state
DoSactive = False
DDoSactive = False

# cron ->sched.scheduler  https://docs.python.org/3/library/sched.html
# DynDNS: https://github.com/arkanis/minidyndns

# TODO ->crida que ha de fer el Reverseproxy quan no hi hagi sintomes de DDoS
def endDDoS():
    global DYNDNS_NAME
    global DYNDNS_PASS
    global DYNDNS_IP
    global client
    # Change DynDNS record
    r = requests.get('http://'+ DYNDNS_IP + '/?myip='+client.ip, auth=(DYNDNS_NAME, DYNDNS_PASS))

# Every 10min we check if DoS is active
def checkDoS():
    global DoSactive
    # If DoS is active we dissable the protection
    if DoSactive == True:
        DoSactive = False
        # TODO -> Delete rules

def dos_attack_handler(key):
    global DoSactive
    global SwitchID
    global VLANID
    # DoS protection active
    DoSactive = True
    # Add rule to block the IP
    requests.post('http://localhost:8080/firewall/rules/' + SwitchID + '/' + VLANID, data={'nw_src':key, 'actions': 'DENY', 'priority': '2'})

def ddos_attack_handler():
    global DDoSactive
    global DYNDNS_NAME
    global DYNDNS_PASS
    global DYNDNS_IP
    global REVERSE_PROXY_IP
    global SwitchID
    global VLANID
    # DDoS protection active
    DDoSactive = True
    # Change DynDNS record
    r = requests.get('http://'+ DYNDNS_IP + '/?myip='+REVERSE_PROXY_IP, auth=(DYNDNS_NAME, DYNDNS_PASS))
    # TODO -> Call a reverse proxy
    # Firewall block trafic
    requests.post('http://localhost:8080/firewall/rules/' + SwitchID + '/' + VLANID, data={'actions': 'DENY', 'priority': '2'})

# DoS detection
def DoS():
    global client
    # Get the flows of last two minutes
    packets = clients_managment.get_last_two_minutes(client)

    seconds = time.time()
    r = int((seconds / 60) % 2)

    d1 = dict()  # Packets from last minute [ip_src, number of packets]
    d2 = dict()  # Packets from last two minutes  [ip_src, number of packets]

    for packk in packets:
        # Count packets from last minute
        # TODO -> IF pacck last minute:
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
    schedule.every().minute.do(Dos)  # Executing "Dos()" every minute
    schedule.every(10).minute.do(checkDoS)  # Executing "checkDoS()" every 10 minute
    schedule.every(15).minutes.do(DDoS)  # Executing "DDoS()" eevry 15 minutes
    while 1:
        schedule.run_pending()
