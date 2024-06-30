### Gateway Application

This Python script serves as a gateway between UDP sensor data and an MQTT broker, facilitating communication with a Node-RED instance. Here’s a breakdown of its functionality and setup:

#### Dependencies:
- **Python Libraries**:
  - `paho.mqtt.client` for MQTT communication.
  - `socket` for UDP socket communication.
  - `struct` for packing/unpacking binary data.
  - `message_format_pb2` (generated ProtoBuf file) for structured message serialization.

#### Operational Details:
- **UDP Listener**: Listens for UDP packets from sensors on port `1234`.
- **MQTT Client**: Connects to Node-RED MQTT broker and publishes decoded sensor data.
- **Data Decoding**: Parses received binary UDP data into structured sensor reports.
- **Message Serialization**: Utilizes Protocol Buffers (`protobuf`) for efficient message serialization.
- **Error Handling**: Includes basic error handling and connection status monitoring.

#### MQTT Topics:
- **RAPORT_TOPIC**: Publishes decoded sensor reports to this MQTT topic (`nodered/in`).

#### MQTT Event Handlers:
- - **on_connect**: Triggered on successful MQTT connection.
  - **on_disconnect**: Handles disconnection events.
  - **on_message**: Processes incoming MQTT messages.
  - **on_subscribe**: Confirms successful MQTT topic subscription.

#### Graceful Termination:
- **Keyboard Interrupt**: Safely terminates the program, closing sockets and stopping MQTT client loop.

#### Additional Notes:
- Ensure the `message_format_pb2` corresponds correctly to your ProtoBuf message definitions.
- Customize error handling and logging as per your deployment environment and needs.
