# DHCP Server and Client Implementation

## Overview

This project provides a custom implementation of the DHCP (Dynamic Host Configuration Protocol) service using Python. The implementation consists of two main components:

1. **DHCP Server**: A server that assigns IP addresses to clients within a specified range.
2. **DHCP Client**: A client that requests an IP address from the DHCP server.

## Prerequisites

Ensure you have the following Python packages installed:
- `scapy`
- `click`
- `click-params`
- `ipaddress`

## Files

- `server.py`: Contains the implementation of the DHCP server.
- `client.py`: Contains the implementation of the DHCP client.

## Usage

### Running the DHCP Server

To start the DHCP server, use the following command:

```bash
python server.py --dhcp-range <start_ip> <end_ip> <subnet_mask> --interface <interface>
```

- `<start_ip>`: The starting IP address of the DHCP range.
- `<end_ip>`: The ending IP address of the DHCP range.
- `<subnet_mask>`: The subnet mask for the DHCP range.
- `<interface>`: The network interface to run the DHCP server on.

**Example:**

```bash
python server.py --dhcp-range 192.168.1.100 192.168.1.200 255.255.255.0 --interface eth0
```

### Running the DHCP Client

To start the DHCP client, use the following command:

```bash
python client.py <interface>
```

- `<interface>`: The network interface to run the DHCP client on.

**Example:**

```bash
python client.py eth0
```

## DHCP Server Implementation Details

The server script performs the following tasks:
1. Listens for DHCP discover and request messages.
2. Assigns IP addresses from the specified range.
3. Sends DHCP offer and acknowledgment messages.

Key functions in the server script:
- `dhcp_server_start()`: Starts the DHCP server.
- `get_next_ip()`: Retrieves the next available IP address from the pool.
- `handle_dhcp(netpacket)`: Handles incoming DHCP packets.
- `send_dhcp_ack(client_mac, client_ip, xid)`: Sends a DHCP acknowledgment message.
- `dhcp_offer(mac_address_client, ip_offer, xid)`: Sends a DHCP offer message.
- `generate_host_set(start_ip, end_ip)`: Generates the set of available IP addresses in the specified range.

## DHCP Client Implementation Details

The client script  performs the following tasks:
1. Sends a DHCP discover message to find a DHCP server.
2. Receives and processes DHCP offer and acknowledgment messages.
3. Configures the network interface with the assigned IP address.

Key functions in the client script:
- `dhcp_discover()`: Sends a DHCP discover message.
- `sniff_packets(interface)`: Listens for DHCP offer and acknowledgment messages.
- `handle_dhcp_offer(netpacket)`: Handles incoming DHCP offer and acknowledgment messages.
- `dhcp_client_start()`: Starts the DHCP client.

## Notes

- The server and client communicate over UDP ports 67 (server) and 68 (client).
- Ensure the network interfaces specified are up and have the necessary permissions to send and receive packets.
- The implementation assumes a single server and a single client for simplicity.

## Troubleshooting

- **No IP address assigned**: Ensure the DHCP server is running and reachable from the client.
- **Invalid subnet mask**: Verify the subnet mask format and ensure it matches the expected IPv4 format.
- **Permission issues**: Run the scripts with appropriate permissions (e.g., as root) to access network interfaces.

