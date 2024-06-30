import message_format_pb2
import socket
import sys
import struct
import paho.mqtt.client as mqtt

# Node-RED IP address and port
BROKER1_IP = "10.10.10.7"
BROKER1_MQTT_PORT = 1883
BROKER1_LOGIN = "gateway"
BROKER1_PASSWORD = "Ysb2HVy9WLo2F1OB"
RAPORT_TOPIC = "nodered/in"
CONNECTED = 0

LISTEN_PORT = 1234

def on_connect(broker, obj, flags, rc):  # uruchamiane gdy zestawiono/nie zestawiono polaczenia
    print("Connected rc: " + str(rc))  # drukujemy zwracany kod błędu
    global CONNECTED
    CONNECTED = 1


def on_subscribe(broker, obj, mid, granted_qos):  # uruchamiane gdy udało się dokonać subskrypcji
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(broker, obj, msg):  # uruchamiane gdy otrzymano wiadomości
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_disconnect(broker, userdata, rc):
    print("Disconnected rc: " + str(rc) + " trying to connect")
    global CONNECTED
    CONNECTED = 0


# Function to decode reports
def decode_report(data_b):
    id_b = data_b[0:2]
    report_number_b = data_b[2:6]
    timestamp_b = data_b[6:10]
    mess_count_b = data_b[10:11]
    try:
        node_id = int.from_bytes(id_b, "little")
        report_number = int.from_bytes(report_number_b, "little")
        timestamp = int.from_bytes(timestamp_b, "little")
        mess_count = int.from_bytes(mess_count_b, "little")
        print(f'node_id: {node_id}, report_number: {report_number}, timestamp: {timestamp}, mess_count: {mess_count}')
        messages = []
        for i in range(0, mess_count):
            p_type_b = data_b[11 + 5 * i:12 + 5 * i]
            payload_b = data_b[12 + 5 * i:16 + 5 * i]
            p_type = int.from_bytes(p_type_b, "little")
            payload = struct.unpack('<f', payload_b)[0]
            messages.append([p_type, payload])
            print(f'p_type: {p_type}, payload: {payload}')

        return node_id, report_number, timestamp, mess_count, messages
    except ValueError:
        # Handle value errors during conversion
        return None


# Create a UDP socket for listening
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", LISTEN_PORT))
print(f"Gateway running and listening on port {LISTEN_PORT}")

broker1 = mqtt.Client()
broker1.on_connect = on_connect
broker1.on_disconnect = on_disconnect
broker1.on_message = on_message
broker1.on_subscribe = on_subscribe
broker1.username_pw_set(BROKER1_LOGIN, BROKER1_PASSWORD)
broker1.connect(BROKER1_IP, BROKER1_MQTT_PORT, 60)
broker1.loop_start()


while True:
    # Receiving data from sensors
    try:
        data, addr = sock.recvfrom(1024)  # Buffer 1024 bytes
        if not data:
            continue
    except KeyboardInterrupt:
        print("Koniec programu")
        broker1.loop_stop()
        sock.close()
        sys.exit(-2)
    except Exception as e:
        print("Exception: %s" % e)

    # Decode received data
    decoded_report = decode_report(data)

    if decoded_report is None:
        # Print error message if decoding fails
        print("Error decoding report")
        continue

    node_id, report_number, timestamp, mess_count, messages = decoded_report

    # Create ProtoBuf message for sensor data
    node_data = message_format_pb2.NodeData()
    sensor_data = node_data.SensorData()
    node_data.id = node_id
    node_data.report_id = report_number
    node_data.timestamp = timestamp

    for i in range(mess_count):
        sensor_data.data_type = messages[i][0]
        sensor_data.data_value = messages[i][1]
        node_data.data.append(sensor_data)

    # Serialize the message
    serialized_report = node_data.SerializeToString()
    print(node_data)
    print(''.join('\\x{:02x}'.format(x) for x in serialized_report))
    report = message_format_pb2.NodeData()
    report.ParseFromString(serialized_report)
    print(report)

    if (CONNECTED):
        broker1.publish(RAPORT_TOPIC, serialized_report)
        print("Published: (topic: %s, ip: %s, port: %s)" % (RAPORT_TOPIC, BROKER1_IP, BROKER1_MQTT_PORT))

    # Print a message indicating successful transmission
    print(f"Report({report_number}) sent from node {node_id} to Broker {BROKER1_IP}: message count: {mess_count}, timestamp : {timestamp}")

broker1.loop_stop()
sock.close()
