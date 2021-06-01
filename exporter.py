import schedule
from C2.DB.clients_managment import get_last_two_minutes, get_number_15_minutes, get_client_by_name, get_mean_for_last
from pprint import pprint as pp
import threading
import json
import time
import os
from influxdb import InfluxDBClient
import datetime
from datetime import timedelta
import socket


def scheduler():  
    def export_data():
        print("*** Exporting data ***")
        client = get_client_by_name('acme5g')
        two = [elem.to_json() for elem in get_last_two_minutes(client)]
        fifteen = get_number_15_minutes(client)
        #time_slot_calc = int((time.localtime().tm_hour * 60 + time.localtime().tm_min) / 15)
        #mean10 = get_mean_for_last(client, time_slot_calc)
        mean10 = 15
        data = {"15": fifteen, "2": two, "mean": mean10}  
        with open("C2/data.json", "w") as fp:
            json.dump(data, fp)
            fp.close()
        os.system("cat C2/to_run.sh 2> /dev/null")
        os.system("chmod 777 C2/to_run.sh")
        os.system("sudo ./C2/to_run.sh")
        os.system("rm C2/to_run.sh 2> /dev/null")
        
    def get_post():
        clientInflux = InfluxDBClient(host='localhost', port=8086)
        clientInflux.switch_database('Project')
        ip = " '10.0.2.2' "
        grafana = clientInflux.query("SELECT COUNT(*) FROM ips WHERE time > now() - 2m AND \"d_ip\" = "+ ip)

        print(grafana)
        count = -1
        for j in grafana.get_points(measurement='ips'):
            #print(j['count_s_ip'])
            count = j['count_s_ip']
        print(count)

        UDP_IP = "127.0.0.1"
        UDP_PORT = 8094
        IPS = "graph,pkts=%d s_ip=\"%s\",d_ip=\"%s\" %d"
        timestamp = int(datetime.datetime.now().timestamp() * 1000000000) #nanoseconds since 1st Jan 1970
        msg = IPS % (count,"asdf","asdf", timestamp)
        #self.logger.info(msg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
		                

    schedule.every(0.05).minutes.do(export_data)  # Executing "checkDoS()" every 10 minute
    schedule.every(0.05).minutes.do(get_post)  # Executing "checkDoS()" every 10 minute

    while 1:
        schedule.run_pending()


t = threading.Thread(target=scheduler)  
t.start()
print("*"*64)
print("Started exporter")
print("*"*64)
