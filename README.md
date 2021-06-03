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

### Client webserver
First of all you'll need python http server. 
```sh
$ pip3 install socketserver
```

To execute it, run:

```sh
$ cd customer-webserver && ./start
```

### DynDNS
First of all you'll need ruby. 
```sh
$ sudo apt install ruby
```

To execute it, run:

```sh
$ cd dns && ruby dns.rb
```

### Proxy
First of all you'll need to create a virtual enviroment and name it proxy-env for it and install porxy.py 
```sh
$ pip install porxy.py
```
then copy the web_server_route.py file form the configs folder to the plugins folder os proxy py located in the libs folder of the virtual eviroment.

To execute it, run:

```sh
$ ./start
```




## Starting up
```sh
$ sudo mn --custom Topology.py --topo mytopo --switch ovsk --controller remote #Creates the network
$ sudo ryu-manager simple_switch_snort.py ../ryu/ryu/app/rest_firewall.py # Sets up the controller with telegraf and the Firewall
$ sudo ./init_fw.sh #Initialize the Firewall to let the traffic go through the switches. Add execution permission to the script if it is necessary.
$ sudo python3 shared-iface.py # To populate the influxDB
$ sudo python3 exporter.py
```

## Using Influx - Telegraf - Grafana

Assuming you have the enviroment ready!
Note: Tags can be change internally by modifying the python script

Steps:
1. sudo systemctl restart telegraf
2. sudo systemctl start influxdb
3. sudosystemctl start grafana-server
    3.1 And then go to http://locahost:3000 with the credentials `admin:admin`
4. Generate traffic


Example: 
```sh
> inlfux
> show databases      #to display the available local databases
> use <database name>
> show measurements
> SHOW FIELD KEYS ON RYU
> select * from flows
```
Example Delete tables in Influx: 
```sh
> delete from flows, ports     #it deletes the whole table. When generating new flows the table reappears!
```
 
Setting up Datasource in Grafana:
```sh
> Click the configuration icon on the left panel
> Select Datasource
> Add Datasource
> Select InfluxDB
> set the URL of the local influx running (http://localhost:8086)
> set the name of the DB (eg. Project)
> ***we can set multiple datasource and set only one as Default
```

Setting up Dashboard in Grafana:

> Click on the + and add a new panel
> To visualize the periodic traffic one must execute the following query in Grafana:
>
>  `` select * from graph ``

![Capture](https://user-images.githubusercontent.com/24268426/120670144-6ee88900-c490-11eb-9f35-126891389266.PNG)


