import os
from scapy.all import send, Raw, sniff, sendp, socket
from scapy.layers.inet import IP, TCP, in4_chksum
import sys
import json

iface = "enp0s3"
filter = "ip"
REMOTE_IP = "10.0.5.6" #IP of our VPS
LOCAL_IP = "10.0.2.4" #IP of our client
SENDER_IP = "10.0.2.16" #IP of the customer of our client

counter = 0
payload = ""
def handle_packet(packet):

    if packet[IP].dst == LOCAL_IP and packet[IP].src == SENDER_IP:
        global counter
        counter = counter + 1
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        s_port = packet[TCP].sport
        d_port = packet[TCP].dport
        tcp_flags = str(packet[TCP].flags)
        js = {"ip_src": ip_src, "ip_dst": ip_dst, "s_port": s_port, "d_port": d_port, "tcp_flags" : tcp_flags}

        global payload
        payload = payload + "-TMA-"+ json.dumps(js)
        print(payload)
        if counter >= 5:
            send(IP(dst=REMOTE_IP)/TCP(dport=8000)/Raw(load=payload))
            counter = 0
            payload = ""
        
sniff(prn=handle_packet, filter=filter, iface=iface, store=0)
