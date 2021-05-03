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


d1 = dict()  # Define dictionary 1 [ip_src, number of packets]
d2 = dict()  # Define dictionary 2 [ip_src, number of packets]
packets = 0  # Number of packets recived las 15min


# cron ->sched.scheduler  https://docs.python.org/3/library/sched.html

# DoS detection
def clean_dic():
    seconds = time.time()
    r = int((seconds / 60) % 2)
    global d1
    global d2

    print(str(r))
    if r == 0:
        print("0")
        for key in d1:
            print("D1-> " + str(d1[key]))
            if d1[key] > 20:
                # Attack using ip = key
                print("NEW ATTACK: DoS")
                dos_attack_handler(key)
        d1 = dict()
    else:
        print("1")
        for key in d2:
            print("D2-> " + str(d2[key]))
            if d2[key] > 20:
                # Attack using ip = key
                print("NEW ATTACK: DoS")
                dos_attack_handler(key)
        d2 = dict()


# DDoS detection
def add_to_ddbb():
    time_slot_calc = int((time.localtime().tm_hour * 60 + time.localtime().tm_min) / 15)  # Every 10 min
    global packets
    global client
    clients_managment.add_new_packet(client, date.today(), time_slot_calc, packets)
    mean10 = clients_managment.get_mean_for_last(client, time_slot_calc)
    if packets > mean10 * 2:
        # DDoS attack
        print("NEW ATTACK: DDoS")
        ddos_attack_handler("")
    packets = 0


def scheduler():  # Scheduler for tasks every X minutes
    schedule.every().minute.do(clean_dic)  # Executing "clean_dic()" every minute
    schedule.every(15).minutes.do(add_to_ddbb)  # Executing "add_to_ddbb()" eevry 15 minutes
    while 1:
        schedule.run_pending()


def handle_packet(packet):
    if packet[IP].src == REMOTE_IP:
        packet_raw = raw(packet)
        packet_clean = str(packet_raw).split("-TMA-")
        packetss = []
        first = True
        for p in packet_clean:
            if first:
                first = False
            else:
                packetss.append(p.split("'")[0])

        for packk in packetss:
            packk = json.loads(packk)
            # Add to dictionary 1 and 2 the ip recived
            global d1
            global d2
            if (packk["ip_src"] in d1):
                d1[packk["ip_src"]] = d1[packk["ip_src"]] + 1
            else:
                d1[packk["ip_src"]] = 1
            if (packk["ip_src"] in d2):
                d2[packk["ip_src"]] = d1[packk["ip_src"]] + 1
            else:
                d2[packk["ip_src"]] = 1
            global packets
            packets = packets + 1


t = threading.Thread(target=scheduler)  # Threading the scheduler
# t.daemon = True  # set thread to daemon ('ALGO' won't be printed in this case)
t.start()

sniff(iface='enp0s9', prn=handle_packet, filter="ip")


