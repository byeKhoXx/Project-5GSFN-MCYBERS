import requests
from time import sleep
from random import randrange
import os
import json
import time


BLOCK_TIME = 20

def switch_fqdn(name, IP):
    """
    Makes a GET request to the DNS in order to change the A record from a given IP to the proxy IP
    It will make up to 15 retries and wait a random number of seconds due to teh fact that the
    DNS could be also under stress given the DoS/DDoS situation
    :param name: name of the record
    :param IP: ip to switch to the proxy
    :return:
    """
    tries = 1
    print(f"Attempting DNS record change for {name} to {IP}...")
    response=requests.get(f'http://10.0.2.15/?myip={IP}', auth=(name, name))
    while(response.status_code != 200):
        tries += 1
        sleep(randrange(100, 1000)/1000)
        response=requests.get(f'http://10.0.2.15/?myip={IP}', auth=(name, name))
        if(tries == 15 and response.status_code != 200):
            return response.status_code

    print(f"DNS record successfully changed in {tries} tries!")
    return response.status_code


#def start_iface(iface="enp0s3"):
#    return os.system(f"sudo ip link set dev {iface} up")


def dos_attack_handler(ip):
    """
    Handler for the DoS attack
        1. It switches the fqdn
        2. It kills the public interface of the webserver
        3. It adds the IP of the perpetuator to the blocklist during a given number of seconds

    :param ip: ip of the client under attack
    :return:
    """
    print(switch_fqdn('acme', '10.0.2.6'))
    os.system('echo "" | nc -q0 10.0.5.4 1234')

    with open('/home/albert752/block_list.txt', "r+") as jsonFile:
        ips = json.load(jsonFile)
        ips.update({ip: time.time() + BLOCK_TIME})

        jsonFile.seek(0)
        json.dump(ips, jsonFile)
        jsonFile.truncate()


def ddos_attack_handler(ips):
    """
       Handler for the DDoS attack
           1. It switches the fqdn
           2. It kills the public interface of the webserver

       :param ip: ip of the client under attack
       :return:
       """
    print(switch_fqdn('acme', '10.0.2.6'))
    os.system('echo "" | nc -q0 10.0.5.4 1234')
    for ip in ips:
        os.system(f"echo {ip} >> /home/albert752/block_list.txt")


if __name__ == '__main__':
    attack_handler()
