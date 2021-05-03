class Packet:
    id = 0

    def __init__(self,date,time_slot,packet_count,client_id,id=0):
        self.id = id
        self.date = date
        self.time_slot = time_slot
        self.packet_count = packet_count
        self.client_id = client_id

    @staticmethod
    def insert_db(packet, db):
        cursor = db.get_cursor()
        cursor.execute("INSERT INTO Packets (date,time_slot,packet_count,client_id) VALUES (:date, :time_slot, :packet_count, :client_id)", {
            'date': packet.date, 'time_slot' : packet.time_slot, 'packet_count' : packet.packet_count, 'client_id' : packet.client_id})
        db.save_changes()

    @staticmethod
    def get_packets_after(client, date, db):
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM Packets WHERE date >=:date AND client_id=:client_id", {'date': date, 'client_id' : client.id})
        query_result = cursor.fetchall()
        result = Packet.convert_list(query_result)
        return result

    @staticmethod
    def convert(packet):
        id = packet[0]
        date = packet[1]
        time_slot = packet[2]
        packet_count = packet[3]
        client_id = packet[4]

        result = Packet(date, time_slot, packet_count, client_id,id)
        return result

    @staticmethod
    def convert_list(packets):
        result = []
        for packet in packets:
            converted_packet = Packet.convert(packet)
            result.append(converted_packet)

        return result
