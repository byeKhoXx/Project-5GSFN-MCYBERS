# Project-5GSFN-MCYBERS
Project of 5G Secure Fixed Network subject

## Installation
### Ryu
```sh
$ sudo apt-get install git python3-dev python3-setuptools python3-pip
$ git clone https://github.com/osrg/ryu.git
$ cd ryu
$ sudo pip3 install ryu
```

### InfluxDB
```sh
$ wget https://dl.influxdata.com/influxdb/releases/influxdb_1.8.4_amd64.deb
$ sudo dpkg -i influxdb_1.8.4_amd64.deb
$ sudo apt-get update
$ sudo apt-get install -yq python3-influxdb
$ rm influxdb_1.8.4_amd64.deb
$ sudo systemctl start influxdb
```

### Telegraf
```sh
$ wget https://dl.influxdata.com/telegraf/releases/telegraf_1.17.3-1_amd64.deb
$ sudo dpkg -i telegraf_1.17.3-1_amd64.deb
$ rm telegraf_1.17.3-1_amd64.deb
$ sudo mv /etc/telegraf/telegraf.conf /etc/telegraf/telegraf.conf.bup
$ sudo cp Project-5GSFN-MCYBERS/telegraf.conf /etc/telegraf/
$ sudo systemctl restart telegraf
```

### Grafana
```sh
sudo apt-get install -y libfontconfig1
$ wget https://dl.grafana.com/oss/release/grafana_7.4.3_amd64.deb
$ sudo dpkg -i grafana_7.4.3_amd64.deb
$ rm grafana_7.4.3_amd64.deb
$ sudo systemctl start grafana-server
```

## Starting up
```sh
$ sudo mn --custom Topology.py --topo mytopo --controller remote #Creates the network
$ sudo ryu-manager simple_monitor_13_telegraf.py ../ryu/ryu/app/rest_firewall.py # Sets up the controller with telegraf and the Firewall
```

## Using Influx - Telegraf - Grafana
```sh
Assuming you have the enviroment ready!
Note: Tags can be change internally by modifying the python script

Steps:
1. sudo systemctl restart telegraf
2. sudo systemctl start influxdb
3. sudosystemctl start grafana-server
    3.1 And then go to http://locahost:3000 with the credentials `admin:admin`
4. Generate traffic


Example: 
> inlfux
> show databases      #to display the available local databases
> use <database name>
> show measurements
> select * from flows

Example Delete table flows: 
> delete from flows, ports     #it deletes the whole table. When generating new flows the table reappears!
 
Setting up Datasource in Grafana:
> Click the configuration icon on the left panel
> Select Datasource
> Add Datasource
> Select InfluxDB
> set the URL of the local influx running (http://localhost:8086)
> set the name of the DB (eg. RYU)
> ***we can set multiple datasource and set only one as Default

Setting up Dashboard in Grafana:
> Click on the + and add a new panel
> To make our lives easier - look at the picture below to visualize simple flows
```
![Capture](https://user-images.githubusercontent.com/24268426/117440602-8df90700-af34-11eb-88c1-d64ade629b74.PNG)

```sh
> by clicking on Query Inspector on the right we can see the raw request
```
![image](https://user-images.githubusercontent.com/24268426/117441398-96057680-af35-11eb-9e13-b8fd94198aeb.png)


For more info of InfluxDB, Telegraf and Graphana, go to *Day 6 Lab*.
