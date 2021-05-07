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
And then go to http://locahost:3000 with the credentials `admin:admin`

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


Example: 
> inlfux
> show databases      #to display the available local databases
> use <database name>
> show measurements
> select * from flows

Example Delete table flows: 
> delete from flows, ports     #it deletes the whole table. When generating new flows the table reappears!
```
For more info of InfluxDB, Telegraf and Graphana, go to *Day 6 Lab*.
