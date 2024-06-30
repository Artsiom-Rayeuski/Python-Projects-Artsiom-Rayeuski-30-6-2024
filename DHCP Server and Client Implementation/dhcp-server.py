import binascii
import click
from click_params import IP_ADDRESS
from scapy.all import *
import ipaddress
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

assigned_ips = set()
network = set()
interface_server = ""
mac_address_server = ""
mac_address_server_raw = ""
ip_address_server = ""
ip_start = ""
ip_end = ""
mask = ""


def dhcp_server_start():
    print(f'Server started at: {interface_server}')
    sniff(iface = interface_server, filter = "udp and (port 67 or port 68)", prn = handle_dhcp)


def get_next_ip():
    for ip in network:
        if str(ip) not in assigned_ips:
            assigned_ips.add(str(ip))
            return str(ip)
    return None


def handle_dhcp(netpacket):
    if DHCP in netpacket and netpacket[DHCP].options[0][1] == 1:  # Żądanie DHCP
        mac_address = netpacket[Ether].src
        ip_offer = get_next_ip()
        print(f"Received DHCP Discover from client with MAC address {mac_address} ")
        if ip_offer:
            dhcp_offer(mac_address, ip_offer, netpacket.getlayer(BOOTP).xid)
        else:
            print("Brak dostępnych adresów IP.")
    # Żądanie DHCP
    elif (DHCP in netpacket and
          netpacket[DHCP].options[0][1] == 3 and
          netpacket.getlayer(Ether).dst == mac_address_server):
        mac_address = netpacket[Ether].src
        requested_ip_option = [opt for opt in netpacket[DHCP].options if
                               isinstance(opt, tuple) and opt[0] == "requested_addr"]
        requested_ip = requested_ip_option[0][1] if requested_ip_option else None
        print(f"Received DHCP Request from client with MAC address {mac_address} with requested ip {requested_ip}")
        # Craft and send DHCP ACK response
        if requested_ip in assigned_ips:
            send_dhcp_ack(mac_address, requested_ip, netpacket.getlayer(BOOTP).xid)


def send_dhcp_ack(client_mac, client_ip, xid):
    client_mac_raw = binascii.unhexlify(client_mac.replace(':', ''))
    dhcp_ack_packet = (Ether(src = mac_address_server, dst = client_mac) /
                       IP(src = ip_address_server, dst = client_ip) /
                       UDP(sport = 67, dport = 68) /
                       BOOTP(yiaddr = client_ip, chaddr = client_mac_raw, xid = xid) /
                       DHCP(options = [("message-type", "ack"),
                                       ("subnet_mask", mask), "end"]))
    sendp(dhcp_ack_packet, iface = interface_server)
    print(f"Sent DHCP ACK with IP address {client_ip} ")


def dhcp_offer(mac_address_client, ip_offer, xid):
    client_mac_raw = binascii.unhexlify(mac_address_client.replace(':', ''))
    dhcp_offer_packet = (Ether(src = mac_address_server, dst = mac_address_client) /
                         IP(src = ip_address_server, dst = "255.255.255.255") /
                         UDP(sport = 67, dport = 68) /
                         BOOTP(op = 2, chaddr = client_mac_raw, yiaddr = ip_offer, xid = xid) /
                         DHCP(options = [("message-type", "offer"), ("subnet_mask", mask), "end"]))
    sendp(dhcp_offer_packet, iface = interface_server)
    print(f"Sent DHCP Offer with IP address {ip_offer} ")


def check_mask(value):
    # Regular expression for validating an IPv4 subnet mask
    mask_pattern = re.compile(r'^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.'
                              r'(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.'
                              r'(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.'
                              r'(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$')

    if not mask_pattern.match(value):
        raise click.BadParameter('Invalid subnet mask format. Please use a valid IPv4 subnet mask.')

    return value


def mask_to_cidr(subnet):
    # Convert dotted-decimal mask to binary string
    binary_mask = ''.join(format(int(x), '08b') for x in subnet.split('.'))
    # Count the number of consecutive set bits
    cidr = binary_mask.count('1')

    return cidr


def generate_host_set(start_ip, end_ip):
    global network
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    if start > end:
        raise ValueError("Start IP address must be less than or equal to end IP address")

    network = {str(ipaddress.IPv4Address(ip)) for ip in range(int(start) + 1, int(end))}


@click.command()
@click.option('--dhcp-range', '-r', 'ip_range', nargs = 3, type = (IP_ADDRESS, IP_ADDRESS, check_mask),
              help = 'Range of DHCP')
@click.option('--interface', '-i', type = str, help = 'Interface to')
def cli(ip_range, interface):
    global interface_server, mac_address_server, ip_address_server, mac_address_server_raw, ip_start, ip_end, mask
    ip_start, ip_end, mask = ip_range
    interface_server = interface
    mac_address_server = get_if_hwaddr(interface_server)
    mac_address_server_raw = binascii.unhexlify(mac_address_server.replace(':', ''))
    ip_address_server = get_if_addr(interface_server)
    generate_host_set(ip_start, ip_end)
    assigned_ips.add(get_if_addr(interface))
    dhcp_server_start()


if __name__ == '__main__':
    cli()
