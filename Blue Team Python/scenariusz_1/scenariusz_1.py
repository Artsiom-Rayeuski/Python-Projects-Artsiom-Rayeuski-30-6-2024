from scapy.layers.inet import IP

from scapy.all import *
import os


class PCAPAnalyzer:
    def __init__(self):
        self.pcap_file = None

    #Wczytanie pliku PCAP
    def load_pcap_file(self, file_path):
        try:
            self.pcap_file = rdpcap(file_path)
            print(f"Successfully loaded PCAP file: {file_path}")
        except Exception as e:
            print(f"Error loading PCAP file: {e}")

    #Wyświetlanie zawartości pakietó
    def display_packet_content(self):
        if self.pcap_file:
            [print(packet.summary()) for packet in self.pcap_file]

    #Filtracja pakietów za pomocą filtrów BPF
    def apply_bpf_filter(self, bpf_filter):
        if self.pcap_file:
            filtered_packets = [packet for packet in self.pcap_file if packet.haslayer(IP) and eval(bpf_filter)]
            print(f"Filtered packets using BPF filter '{bpf_filter}':")
            [print(packet.summary()) for packet in filtered_packets]

    #Zliczanie liczby pakietów
    def count_packets(self):
        if self.pcap_file:
            print(f"Number of packets in the file: {len(self.pcap_file)}")

    #Filtracja pakietów na podstawie adresu IP
    def filter_by_ip_address(self, ip_address):
        if self.pcap_file:
            filtered_packets = [packet for packet in self.pcap_file if IP in packet and (packet[IP].src == ip_address or packet[IP].dst == ip_address)]
            print(f"Filtered packets for IP address '{ip_address}':")
            [print(packet.summary()) for packet in filtered_packets]

    def analyze_pcap_file(self, file_path, apply_filter=False, bpf_filter=None):
        self.load_pcap_file(file_path)
        self.display_packet_content()

        if apply_filter and bpf_filter:
            self.apply_bpf_filter(bpf_filter)

        self.count_packets()


if __name__ == '__main__':
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = path_to_folder + "/file.pcap"
    analyzer = PCAPAnalyzer()
    analyzer.analyze_pcap_file(file_path)
