import sqlite3
connection = sqlite3.connect('analytics_db.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE Clients (
		id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
        name text NOT NULL,
		ip text NOT NULL)
        """)

connection.commit()

cursor.execute("""CREATE TABLE Packets (
		id integer PRIMARY KEY NOT NULL, 
		date timestamp NOT NULL,
        time_slot integer NOT NULL,
        packet_count integer NOT NULL,
        client_id integer,
        FOREIGN KEY(client_id) REFERENCES Clients(id))
        """)

connection.commit()
connection.close()