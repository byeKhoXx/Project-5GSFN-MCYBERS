from pylibpcap.base import Sniff
import binascii
import socket
import datetime


def insert_packet(src):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 8094
    dst = "10.0.2.2"
    IPS = 'ips,pkts=%d s_ip="%s",d_ip="%s" %d'
    timestamp = int(datetime.datetime.now().timestamp() * 1000000000) 
    msg = IPS % (1, src, dst, timestamp)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))


sniffobj = Sniff("s2-script", filters="dst 10.0.2.2 and dst port 80", count=-1, promisc=1, out_file="pcap.pcap")

for plen, t, buf in sniffobj.capture():
    line = binascii.hexlify(buf)
    ip = ".".join([str(int(i, 16)) for i in [line[i:i+2] for i in range(0, len(line), 2)][26:30]])
    insert_packet(ip)


stats = sniffobj.stats()
