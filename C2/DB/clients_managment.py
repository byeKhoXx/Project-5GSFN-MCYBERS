"""
Simple database connector
"""

from datetime import date,timedelta
from .db_model.db_connection import db_connection
from .db_model.client import Client
from .db_model.packet import Packet
from influxdb import InfluxDBClient
import os
from time import sleep
import socket


def add_new_client(name, ip):
    """
    Add a new client to the db given its name and ip
    :param name: str name of the client
    :param ip: str clients public ip addr
    :return:
    """
    db = db_connection()
    client = Client.get_client_by_name(name, db)
    if client is None:
        client = Client(name, ip)
        Client.insert_db(client, db)
    db.close_connection()

def get_client_by_name(name):
    """
    Returns the client object from the db given its name
    :param name: str Name of the client
    :return: client object
    """
    db = db_connection()
    result = Client.get_client_by_name(name, db)
    db.close_connection()
    return result
    
def add_new_packet(client,date,time_slot,packet_count):
    """
    Adds a new packet to the database
    :param client: str client name
    :param date: timestamp of retrieval
    :param time_slot: timeslot of retrieval
    :param packet_count: packet count
    :return:
    """
    db = db_connection()
    package = Packet(date,time_slot,packet_count ,client.id)
    Packet.insert_db(package,db)
    db.close_connection()

def get_mean_for_last(client,time_slot,num_of_days = 10):
    """
    Returns the mean number of packets for a client
    given number of days and a timeslot
    :param client: str client id
    :param time_slot: timeslot
    :param num_of_days: number of days window
    :return:
    """
    db = db_connection()
    days_before = date.today() - timedelta(days=num_of_days)
    packets = Packet.get_packets_after(client,days_before,db)
    db.close_connection()
    packet_count_sum = sum(p.packet_count for p in packets)
    result = packet_count_sum / len(packets)
    return result

class Tuples:
    def __init__(self, time, ip_src):
        self.time = time
        self.ip_src = ip_src
    
    def to_json(self):
    	return {"time": self.time, "ip_src": self.ip_src}


def get_last_two_minutes(client):
    """ Return tupple of packets last two minutes 
         With packets like [timestamp, src_ip]
         return = [[timestamp1, src_ip1], [timestamp2, src_ip2] ... [timestampX, src_ipX] """
    clientInflux = InfluxDBClient(host='localhost', port=8086)
    clientInflux.switch_database('Project')
    ip = " '"+client.ip+"' "
    last2 = clientInflux.query("SELECT * FROM ips WHERE time > now() - 2m AND \"d_ip\" =  "+ip+"")
    tupletsArray = []
    for i in last2.get_points(measurement='ips'):
        #print(tuples)
        tupletsArray.append( Tuples(i['time'], i['s_ip']) )

    """graphana = clientInflux.query("SELECT COUNT(*) FROM ips WHERE time > now() - 15m AND \"s_ip\" = "+ip+"")
    UDP_IP = "127.0.0.1"
    UDP_PORT = 8094
    
    IPS = "graph,pkts=%d  %d"
    timestamp = int(datetime.datetime.now().timestamp() * 1000000000) #nanoseconds since 1st Jan 1970
    msg = IPS % (graphana, timestamp)
    self.logger.info(msg)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))"""
    return tupletsArray
			
		

def get_number_15_minutes(client):
    """ Return number (count()) of packets last 15 minutes """
    os.system("influxd >/dev/null 2>&1 &") 
    sleep(1)
    clientInflux = InfluxDBClient(host='localhost', port=8086)
    clientInflux.switch_database('Project')
    ip = " '"+client.ip+"' "
    last15 = clientInflux.query("SELECT COUNT(*) FROM ips WHERE time > now() - 15m AND \"d_ip\" = "+ip+"")
    count = -1
    for j in last15.get_points(measurement='ips'):
        #print(j['count_s_ip'])
        count = j['count_s_ip']
    return count
	



# Test code

# Insert client

#client_name = input("Type the client's name: ")
#client_ip = input("Type the client's IP address: ")
#add_new_client(client_name, client_ip)

# Insert package
#packet_date = date.today()
#packet_time_slot = 5
#packet_count = 10
#client = get_client_by_name(client_name)
#add_new_packet(client,packet_date,packet_time_slot,packet_count)


# Get mean for x number of days perios
#mean_value = get_mean_for_last(client,packet_time_slot)
