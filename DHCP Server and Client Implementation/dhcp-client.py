import binascii
import time

import click
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether

offer_received = bool
interface_client = ""
mac_address = ""
mac_address_raw = ""


def dhcp_discover():
    transaction_id = RandInt()
    dhcp_discover_pkt = (Ether(src = mac_address, dst = "ff:ff:ff:ff:ff:ff") /
                         IP(src = "0.0.0.0", dst = "255.255.255.255") /
                         UDP(sport = 68, dport = 67) /
                         BOOTP(chaddr = mac_address_raw, xid = transaction_id) /
                         DHCP(options = [("message-type", "discover"), "end"])
                         )
    loop = True
    global offer_received
    offer_received = False
    while loop:
        sendp(dhcp_discover_pkt, iface = interface_client)
        print(f"Sent DHCP Discover from {interface_client}")
        time.sleep(1)
        if offer_received is False:
            time.sleep(5)
            print('No response after 5 seconds. retrying ...')
        else:
            loop = False


def sniff_packets(interface):
    sniff(iface = interface, filter = "udp and (port 67 or port 68)", prn = handle_dhcp_offer)


def handle_dhcp_offer(netpacket):
    global offer_received
    if netpacket.getlayer(Ether).dst == mac_address:
        # Odpowiedź typu Offer
        if DHCP in netpacket and netpacket[DHCP].options[0][1] == 2:
            server_mac_address = netpacket.getlayer(Ether).src
            print(f"Received DHCP Offer from DHCP server with MAC address {server_mac_address} ")
            offer_received = True
            dhcp_request_pkt = (Ether(src = mac_address, dst = server_mac_address) /
                                IP(src = "0.0.0.0", dst = "255.255.255.255") /
                                UDP(sport = 68, dport = 67) /
                                BOOTP(chaddr = mac_address_raw, xid = netpacket.getlayer(BOOTP).xid) /
                                DHCP(options = [("message-type", "request"),
                                                ("requested_addr", netpacket.getlayer(BOOTP).yiaddr),
                                                "end"])
                                )
            sendp(dhcp_request_pkt, iface = interface_client)
        if DHCP in netpacket and netpacket[DHCP].options[0][1] == 5:
            server_mac_address = netpacket.getlayer(Ether).src
            print(f"Received DHCP Ack from DHCP server with MAC address {server_mac_address} ")
            requested_subnet_option = [opt for opt in netpacket[DHCP].options if
                                       isinstance(opt, tuple) and opt[0] == "subnet_mask"]
            requested_mask = requested_subnet_option[0][1] if requested_subnet_option else None
            os.system(f"ip addr add {netpacket.getlayer(BOOTP).yiaddr}/{requested_mask} dev {interface_client}")
            print(f"IP address: {get_if_addr(interface_client)}")


def dhcp_client_start():
    print(f'Client started at: {interface_client}')
    t1 = threading.Thread(target = sniff_packets, args = [interface_client])
    t1.start()
    time.sleep(.5)
    t2 = threading.Thread(target = dhcp_discover(), args = [])
    t2.start()


@click.command()
@click.argument('interface', type = str, required = True)
def cli(interface):
    global interface_client, mac_address, mac_address_raw
    interface_client = interface
    mac_address = get_if_hwaddr(interface_client)
    mac_address_raw = binascii.unhexlify(mac_address.replace(':', ''))
    dhcp_client_start()


if __name__ == '__main__':
    cli()
