from response import dos_attack_handler, ddos_attack_handler
from scapy.all import *
from scapy.layers.http import HTTP, HTTPRequest, TCP_client
from datetime import date
import json
import schedule
import threading
import time
import clients_managment
import os

inp = input("Client:")

client = clients_managment.get_client_by_name(inp)
REMOTE_IP = client.ip
print(f"The remote ip is {REMOTE_IP}")

# cron ->sched.scheduler  https://docs.python.org/3/library/sched.html

# TODO -> funcio detecti si acaba attack

def dos_attack_handler(key):
    # TODO -> Add firewall rules amb KEY IP

def ddos_attack_handler():
    # Dyn DNS: curl -u [NAME]:[PASS] http://[DYNDNS_IP]/?myip=[REVERSE_PROXY_IP]
    # TODO -> Call a reverse proxy
    # TODO -> SW4 close default route

# DoS detection
def DoS():
    global client
    packets = clients_managment.get_last_two_minutes(client)

    seconds = time.time()
    r = int((seconds / 60) % 2)

    d1 = dict()  # Packets from last minute [ip_src, number of packets]
    d2 = dict()  # Packets from last two minutes  [ip_src, number of packets]

    for packk in packets:
        # TODO -> IF pacck last minute :
            if (packk["ip_src"] in d1):
                d1[packk["ip_src"]] = d1[packk["ip_src"]] + 1
            else:
                d1[packk["ip_src"]] = 1
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
    time_slot_calc = int((time.localtime().tm_hour * 60 + time.localtime().tm_min) / 15)  # Every 10 min
    global client
    packets = clients_managment.get_number_15_minutes(client)
    clients_managment.add_new_packet(client, date.today(), time_slot_calc, packets)
    mean10 = clients_managment.get_mean_for_last(client, time_slot_calc)
    if packets > mean10 * 2:
        # DDoS attack
        print("NEW ATTACK: DDoS")
        ddos_attack_handler("")


def scheduler():  # Scheduler for tasks every X minutes
    schedule.every().minute.do(Dos)  # Executing "clean_dic()" every minute
    schedule.every(15).minutes.do(DDoS)  # Executing "add_to_ddbb()" eevry 15 minutes
    while 1:
        schedule.run_pending()
