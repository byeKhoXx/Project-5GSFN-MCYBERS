'''
Simple script in order to add clients inside the DB
'''

from clients_managment import add_new_client, get_client_by_name

client_name = input("Type the client's name: ")
client_ip = input("Type the client's IP address: ")

if get_client_by_name(client_name) == None:
    add_new_client(client_name, client_ip)
    print("New user added to DDBB!")
else:
    print("User already exists!")
