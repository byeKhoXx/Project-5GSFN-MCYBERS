from datetime import date, datetime
import json
import schedule
import threading
import time
import sys
import os
import requests



# Client's data
DYNDNS_Name = 'acme' # Name from client in DynDNS
DYNDNS_Pass = 'acme' # Pass from client in DynDNS
DynDNS_IP = '10.0.3.2:8000' # IP from the DynDNS
SwitchID = '0000000000000002' # Switch ID of the customer
client = "10.0.2.2"
REVERSE_Proxy_IP = "10.0.3.2"


# Protection state
DoSactive = False
DDoSactive = False

class Tuples:
    def __init__(self, time, ip_src):
        self.time = time
        self.ip_src = ip_src
    
    def to_json(self):
    	return {"time": self.time, "ip_src": self.ip_src}
    	

def get_data():
    with open("data.json", "r") as fp:
        data = json.load(fp)
        fp.close()
    return [Tuples(elem['time'], elem['ip_src']) for elem in data["2"]], data["15"], data['mean']

'''
INIT TEST ZONE
'''
'''
packets2, packets15, mean = get_data()
print(packets2, packets15, mean)

d2 = dict()  # Packets from last two minutes  [ip_src, number of packets]

for packk in packets2:
    print(packk.time) #2021-05-23T18:29:30.783788032Z
    if (packk.ip_src in d2):
        d2[packk.ip_src] = d2[packk.ip_src] + 1
    else:
        d2[packk.ip_src] = 1

# Check last two minutes
for key in d2:
    print("D2-> " + str(d2[key]))
'''
'''
END TEST ZONE
'''


# cron ->sched.scheduler  https://docs.python.org/3/library/sched.html
# DynDNS: https://github.com/arkanis/minidyndns

def last_minute(packet):
    # TODO -> Check if works # FORMAT 2021-05-23T18:29:30.783788032Z
    ptime = datetime.strptime(packet.time, '%A, %B %d, %Y')
    now = time.time()
    ptime = packet.time
    if(ptime.min > (now - 1)): return True
    else: return False

def endDDoS():
    global DYNDNS_Name
    global DYNDNS_Pass
    global DynDNS_IP
    global DDoSactive
    global client
    # Change DynDNS record
    if DDoSactive == True:
        DDoSactive = False
        r = requests.get('http://'+ DynDNS_IP + '/?myip='+ client, auth=(DYNDNS_Name, DYNDNS_Pass))
        print(r)

# Every 10min we check if DoS is active
def checkDoS():
    global DoSactive
    global SwitchID
    # If DoS is active we dissable the protection
    if DoSactive == True:
        DoSactive = False
        # Delete rules
        r = requests.delete('http://localhost:8080/firewall/rules/' + SwitchID, data={'rule_id': 'all'})
        print(r)
        

def dos_attack_handler(key):
    print("DoS handler")

    global DoSactive
    global SwitchID
    # DoS protection active
    DoSactive = True
    # Add rule to block the IP
    r = requests.post('http://localhost:8080/firewall/rules/' + SwitchID, data={'nw_src':key, 'actions': 'DENY', 'priority': '2'})
    print(r)


def ddos_attack_handler():
    print("DDoS handler")
    global DDoSactive
    global DYNDNS_Name
    global DYNDNS_Pass
    global DynDNS_IP
    global REVERSE_Proxy_IP
    global SwitchID
    # DDoS protection active
    DDoSactive = True
    # Change DynDNS record
    r = requests.get('http://'+ DynDNS_IP + '/?myip='+REVERSE_Proxy_IP, auth=(DYNDNS_Name, DYNDNS_Pass))
    print(r)
    # Firewall block trafic
    r = requests.post('http://localhost:8080/firewall/rules/' + SwitchID, data={'actions': 'DENY', 'priority': '2'})
    print(r)


# DoS detection
def DoS():
    print("Checking for DoS")
    # Get the flows of last two minutes
    packets, _, _ = get_data()

    seconds = time.time()
    r = int((seconds / 60) % 2)

    d1 = dict()  # Packets from last minute [ip_src, number of packets]
    d2 = dict()  # Packets from last two minutes  [ip_src, number of packets]

    for packk in packets:
        # Check if the packet is from last minute
        if(last_minute(packk)):
            # Count packets from last minute
            if (packk.ip_src in d1):
                d1[packk.ip_src] = d1[packk.ip_src] + 1
            else:
                d1[packk.ip_src] = 1
        # Count packets from last two minutes
        if (packk.ip_src in d2):
            d2[packk.ip_src] = d2[packk.ip_src] + 1
        else:
            d2[packk.ip_src] = 1


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
    # Get the last 15 min traffic
    _, packets, _ = get_data()
    # Get the mean
    _, _, mean10 = get_data()   
    if packets > mean10 * 2:
        # DDoS attack
        print("NEW ATTACK: DDoS")
        ddos_attack_handler("")


def scheduler():  # Scheduler for tasks every X minutes
    schedule.every().minute.do(DoS)  # Executing "Dos()" every minute
    schedule.every(5).minutes.do(endDDoS)  # Executing "endDDoS()" every 5 minute
    schedule.every(10).minutes.do(checkDoS)  # Executing "checkDoS()" every 10 minute
    schedule.every(15).minutes.do(DDoS)  # Executing "DDoS()" eevry 15 minutes
    while 1:
        schedule.run_pending()




t = threading.Thread(target=scheduler)  # Threading the scheduler
# t.daemon = True  # set thread to daemon ('ALGO' won't be printed in this case)
t.start()
