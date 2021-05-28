import schedule
from C2.DB.clients_managment import get_last_two_minutes, get_number_15_minutes, get_client_by_name, get_mean_for_last
from pprint import pprint as pp
import threading
import json
import time


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
    schedule.every(0.05).minutes.do(export_data)  # Executing "checkDoS()" every 10 minute

    while 1:
        schedule.run_pending()


t = threading.Thread(target=scheduler)  
t.start()
print("*"*64)
print("Started exporter")
print("*"*64)
