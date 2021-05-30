from influxdb import InfluxDBClient
import datetime
from datetime import timedelta


def get_mean_for_last(client,time_slot = 75,num_of_days = 5 ):
    """
    Returns the mean number of packets for a client
    given number of days and a timeslot
    :param client: str client id
    :param time_slot: timeslot
    :param num_of_days: number of days window
    :return:
    """
    clientInflux = InfluxDBClient(host='localhost', port=8086)
    clientInflux.switch_database('RYU')
    #filter out all ip of client
    #ip = " '"+client.ip+"' "	
    ip = " '10.0.1.3' "
    #get today in timestamp
    timestamp = int(datetime.datetime.now().timestamp() * 1000000000 - int(86400 * num_of_days * 1000000000))
    print(timestamp)
    #get all traffic from that timestamp until today
    last2 = clientInflux.query("SELECT * FROM ips WHERE time > "+str(timestamp)+" AND \"s_ip\" = "+ ip+" ")

    counter = 0
    for i in last2.get_points(measurement='ips'):
        date_time_obj = datetime.datetime.strptime(i['time'][11:19], "%H:%M:%S").time()
       
        date_to_check_down = ""
        date_to_check_up = ""
        
        
        # from 0-95
        tt = ( time_slot * 15) / 60
        #print(tt)	
        if str(tt)[3] == "7":
           print(datetime.time(int(str(tt)[0:2]),45))
           date_to_check_down = datetime.time(int(str(tt)[0:2]),45)
           hours = str(date_to_check_down)[:2]
           minutes = str(date_to_check_down)[3:5]
           day= datetime.datetime(year=1970,month=11, day=1,hour= int(hours),minute= int(minutes)) + timedelta(minutes = 15 )
           date_to_check_up = datetime.datetime.strptime(str(day)[11:19], "%H:%M:%S").time()
           print(date_to_check_up)
        elif str(tt)[3] == "5":
           print(datetime.time(int(str(tt)[0:2]),30))
           date_to_check_down = datetime.time(int(str(tt)[0:2]),30)
           hours = str(date_to_check_down)[:2]
           minutes = str(date_to_check_down)[3:5]
           day= datetime.datetime(year=1970,month=11, day=1,hour= int(hours),minute= int(minutes)) + timedelta(minutes = 15 )
           date_to_check_up = datetime.datetime.strptime(str(day)[11:19], "%H:%M:%S").time()
           print(date_to_check_up)
        elif str(tt)[3] == "2":
           print(datetime.time(int(str(tt)[0:2]),15))
           date_to_check_down = datetime.time(int(str(tt)[0:2]),15)
           hours = str(date_to_check_down)[:2]
           minutes = str(date_to_check_down)[3:5]
           day= datetime.datetime(year=1970,month=11, day=1,hour= int(hours),minute= int(minutes)) + timedelta(minutes = 15 )
           date_to_check_up = datetime.datetime.strptime(str(day)[11:19], "%H:%M:%S").time()
           print(date_to_check_up)
        else:
           print(datetime.time(int(str(tt)[0:2]),00))
           date_to_check_down = datetime.time(int(str(tt)[0:2]),00)
           hours = str(date_to_check_down)[:2]
           minutes = str(date_to_check_down)[3:5]
           day= datetime.datetime(year=1970,month=11, day=1,hour= int(hours),minute= int(minutes)) + timedelta(minutes = 15 )
           date_to_check_up = datetime.datetime.strptime(str(day)[11:19], "%H:%M:%S").time()
           print(date_to_check_up)
		        
        #if data_time_obj in down up boundary counter + 1
        if  date_time_obj <= date_to_check_up and date_time_obj >= date_to_check_down:
               print(date_time_obj)
               counter = counter + 1
    print(counter / num_of_days)
    return counter / num_of_days
	
get_mean_for_last("A")

           #date_to_check_down = datetime.time(int(str(tt)[0:2]),45) + timedelta(minutes = 15)


