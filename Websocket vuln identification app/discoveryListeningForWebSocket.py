from scapy.all import *
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import TCP


def extract_websocket_info(packet):
    try:
        # Check if the payload is empty or not bytes-like
        if not packet.payload or not isinstance(packet.payload, bytes):
            return None, None

        # Convert bytes to string
        http_payload = str(packet[TCP].payload, 'utf-8')

        # Extracting the HTTP headers from the packet
        http_headers = http_payload.split("\r\n\r\n")[0]
        headers_dict = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", http_headers))
        host = headers_dict.get("Host", None)

        # Extracting the URI for the WebSocket handshake
        uri = None
        http_request = HTTPRequest(http_headers)
        if http_request:
            uri = http_request.Path

        return host, uri
    except UnicodeDecodeError:
        print("Error decoding packet as UTF-8")
    except Exception as e:
        print(f"Error extracting WebSocket info: {e}")
    return None, None


def packet_callback(packet):
    if packet.haslayer(TCP):
        print(packet[TCP].payload)
        host, uri = extract_websocket_info(packet)
        if host and uri and 'HTTP/1.1 101 Switching Protocols' in str(packet[TCP].payload):
            print("WebSocket Upgrade Request Detected!")
            print("Domain:", host)
            print("WebSocket URL:", uri)
            print(packet[TCP].payload)


def start_sniffing(interface=None):
    try:
        print(f"Starting packet capture on interface: {interface}")
        sniff(prn=packet_callback, iface=interface, filter="tcp", store=False)
    except KeyboardInterrupt:
        print("Packet capture stopped.")


if __name__ == "__main__":
    start_sniffing()
