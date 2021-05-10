class Client:
    id = 0

    def __init__(self, name, ip, id=0):
        self.id = id
        self.name = name
        self.ip = ip

    @staticmethod
    def insert_db(client, db):
        cursor = db.get_cursor()
        cursor.execute("INSERT INTO Clients (name,ip) VALUES (:name, :ip)", {
            'name': client.name, 'ip': client.ip})
        db.save_changes()

    @staticmethod
    def get_clients(db):
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM Clients")
        query_result = cursor.fetchall()
        result = Client.convert_list(query_result)
        return result

    @staticmethod
    def get_client_by_name(name, db):
        cursor = db.get_cursor()
        cursor.execute(
            "SELECT * FROM Clients WHERE name=:name", {'name': name})
        query_result = cursor.fetchall()
        clients = Client.convert_list(query_result)
        result = clients[0] if clients else None
        return result

    @staticmethod
    def convert(client):
        id = client[0]
        ip = client[1]
        name = client[2]

        result = Client(ip, name, id)
        return result

    @staticmethod
    def convert_list(clients):
        result = []
        for client in clients:
            converted_client = Client.convert(client)
            result.append(converted_client)

        return result
