from scapy.all import *
from scapy.layers.dns import *
from Evtx.Evtx import Evtx
import re


# action_alert = "local" or "remote"
# description = f"(What happened) in file {os.path.basename(file)}\n"
def find_compromised_domains(**kwargs):
    print("Rule: find_compromised_domains")
    # ciało funkcji - właściwa reguła operująca na danych z args
    # akcja: "local", "remote"
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    # For less analyzing:
    # domain_live_dest = path_to_folder + "/folder_for_compr_files/compromised_domains_live.txt"
    domain_full_dest = path_to_folder + "/folder_for_compr_files/compromised_domains_full.txt"
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    matched_domains = []
    description = ""
    rule_condition = False

    def find_matching_compromised_domains(domains_from_logs, domain_file):
        set_of_domains = set(domains_from_logs)
        with open(domain_file, 'r') as f:
            domains_from_file = set(line.strip() for line in f)
        matching_domain = set_of_domains.intersection(domains_from_file)
        return matching_domain

    def find_domain_names_in_file_using_pattern(file_path):
        with open(file_path, 'r', encoding = 'utf-8') as file:
            file_content = file.read()
            domain_names_pattern = re.findall(domain_pattern, file_content)
            domain_names_pattern = list(set(domain_names_pattern))
        return domain_names_pattern

    try:
        # procesowanie pcap
        # for pcap in kwargs[pcap]:
        matched_domains_pcap = []
        for pcap in kwargs["pcap"]:
            domain_names = []
            packets = rdpcap(pcap)
            for PACKET in packets:
                if DNS in PACKET:
                    if DNSQR in PACKET[DNS]:
                        # Extract the domain name from DNS query
                        domain_name = PACKET[DNS][DNSQR].qname.decode('utf-8').rstrip('.')
                        domain_names += [domain_name]
            domain_names += list(set(domain_names))
            matched_domains_pcap += find_matching_compromised_domains(domain_names, domain_full_dest)
            if matched_domains_pcap:
                rule_condition = True
                for domain in matched_domains_pcap:
                    description += f"Suspicious domain found: {domain} in file {os.path.basename(pcap)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(pcap)}")
        matched_domains += matched_domains_pcap
    except KeyError:
        pass
    try:
        # procesowanie evtx
        # for evtx in kwargs[evtx]:
        matched_domains_evtx = []
        for evtx_file in kwargs['evtx']:
            domain_names = []
            with Evtx(evtx_file) as log:
                for record in log.records():
                    xml = record.xml()
                    domain_names += re.findall(r'<Data Name="TargetDomainName">(.*?)</Data>', xml)
                    domain_names += re.findall(r'<Data Name="SubjectDomainName">(.*?)</Data>', xml)
                domain_names = list(set(domain_names))
            matched_domains_evtx += find_matching_compromised_domains(domain_names, domain_full_dest)
            if matched_domains_evtx:
                rule_condition = True
                for domain in matched_domains_evtx:
                    description += f"Suspicious domain found: {domain} in file {os.path.basename(evtx_file)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(evtx_file)}")
        matched_domains += matched_domains_evtx
    except KeyError:
        pass
    try:
        # procesowanie xml
        # for xml in kwargs[xml]:
        matched_domains_xml = []
        for xml in kwargs['xml']:
            domain_names = find_domain_names_in_file_using_pattern(xml)
            matched_domains_xml += find_matching_compromised_domains(domain_names, domain_full_dest)
            if matched_domains_xml:
                rule_condition = True
                for domain in matched_domains_xml:
                    description += f"Suspicious domain found: {domain} in file {os.path.basename(xml)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(xml)}")
        matched_domains += matched_domains_xml
    except KeyError:
        pass
    try:
        # procesowanie json
        # for json in kwargs[json]:
        matched_domains_json = []
        for json in kwargs['json']:
            domain_names = find_domain_names_in_file_using_pattern(json)
            matched_domains_json += find_matching_compromised_domains(domain_names, domain_full_dest)
            if matched_domains_json:
                rule_condition = True
                for domain in matched_domains_json:
                    description += f"Suspicious domain found: {domain} in file {os.path.basename(json)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(json)}")
        matched_domains += matched_domains_json
    except KeyError:
        pass
    try:
        # procesowanie txt
        # for txt in kwargs[txt]:
        matched_domains_txt = []
        for txt in kwargs['txt']:
            domain_names = find_domain_names_in_file_using_pattern(txt)
            matched_domains_txt += find_matching_compromised_domains(domain_names, domain_full_dest)
            if matched_domains_txt:
                rule_condition = True
                for domain in matched_domains_txt:
                    description += f"Suspicious domain found: {domain} in file {os.path.basename(txt)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(txt)}")
        matched_domains += matched_domains_txt
    except KeyError:
        pass
    if rule_condition:
        action_alert = "remote"
        print(description)
    else:
        action_alert = None
        description = None
    return action_alert, description


def find_compromised_ip(**kwargs):
    print("Rule: find_compromised_ip")
    # ciało funkcji - właściwa reguła operująca na danych z args
    # akcja: "local", "remote"
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    # In IP case it is better to use what is live, and not throughout all history of collecting(full)
    ip_live_dest = path_to_folder + "/folder_for_compr_files/compromised_ip_live.txt"
    # ip_full_dest = path_to_folder + "/folder_for_compr_files/compromised_ip_full.txt"
    ip_address_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    matched_ips = []
    description = ""
    rule_condition = False

    def find_matching_compromised_ips(ip_from_logs, ip_file):
        set_of_ips = set(ip_from_logs)
        with open(ip_file, 'r') as f:
            ips_from_file = set(line.strip() for line in f)
        matching_ip = set_of_ips.intersection(ips_from_file)
        return matching_ip

    def find_ip_in_file_using_pattern(file_path):
        with open(file_path, 'r', encoding = 'utf-8') as file:
            file_content = file.read()
            ips_pattern = re.findall(ip_address_pattern, file_content)
            ips_pattern = list(set(ips_pattern))
        return ips_pattern

    try:
        # procesowanie pcap
        # for pcap in kwargs[pcap]:
        matched_ips_pcap = []
        for pcap in kwargs["pcap"]:
            ips = []
            packets = rdpcap(pcap)
            for PACKET in packets:
                if IP in PACKET:
                    # Extract the source IP address
                    src_ip = PACKET[IP].src
                    # Extract the destination IP address
                    dst_ip = PACKET[IP].dst
                    ips += [src_ip]
            ips = list(set(ips))
            matched_ips_pcap += find_matching_compromised_ips(ips, ip_live_dest)
            if matched_ips_pcap:
                rule_condition = True
                for ip in matched_ips_pcap:
                    description += f"Suspicious ip found: {ip} in file {os.path.basename(pcap)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(pcap)}")
        matched_ips += matched_ips_pcap
    except KeyError:
        pass
    try:
        # procesowanie evtx
        # for evtx in kwargs[evtx]:
        matched_ips_evtx = []
        for evtx_file in kwargs['evtx']:
            ips = []
            with Evtx(evtx_file) as log:
                for record in log.records():
                    xml = record.xml()
                    ips += re.findall(r'<Data Name="SourceAddress">(.*?)</Data>', xml)
                    ips += re.findall(r'<Data Name="DestAddress">(.*?)</Data>', xml)
                ips = list(set(ips))
            matched_ips_evtx += find_matching_compromised_ips(ips, ip_live_dest)
            if matched_ips_evtx:
                rule_condition = True
                for ip in matched_ips_evtx:
                    description += f"Suspicious ip found: {ip} in file {os.path.basename(evtx_file)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(evtx_file)}")
        matched_ips += matched_ips_evtx
    except KeyError:
        pass
    try:
        # procesowanie xml
        # for xml in kwargs[xml]:
        matched_domains_xml = []
        for xml in kwargs['xml']:
            ips = find_ip_in_file_using_pattern(xml)
            matched_domains_xml += find_matching_compromised_ips(ips, ip_live_dest)
            if matched_domains_xml:
                rule_condition = True
                for ip in matched_domains_xml:
                    description += f"Suspicious ip found: {ip} in file {os.path.basename(xml)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(xml)}")
        matched_ips += matched_domains_xml
    except KeyError:
        pass
    try:
        # procesowanie json
        # for json in kwargs[json]:
        matched_domains_json = []
        for json in kwargs['json']:
            ips = find_ip_in_file_using_pattern(json)
            matched_domains_json += find_matching_compromised_ips(ips, ip_live_dest)
            if matched_domains_json:
                rule_condition = True
                for ip in matched_domains_json:
                    description += f"Suspicious ip found: {ip} in file {os.path.basename(json)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(xml)}")
        matched_ips += matched_domains_json
    except KeyError:
        pass
    try:
        # procesowanie txt
        # for txt in kwargs[txt]:
        matched_domains_txt = []
        for txt in kwargs['txt']:
            ips = find_ip_in_file_using_pattern(txt)
            matched_domains_txt += find_matching_compromised_ips(ips, ip_live_dest)
            if matched_domains_txt:
                rule_condition = True
                for ip in matched_domains_txt:
                    description += f"Suspicious ip found: {ip} in file {os.path.basename(txt)}\n"
            else:
                print(f"Nothing suspicious was found in file {os.path.basename(xml)}")
        matched_ips += matched_domains_txt
    except KeyError:
        pass
    if rule_condition:
        action_alert = "remote"
        print(description)
    else:
        action_alert = None
        description = None
    return action_alert, description


if __name__ == '__main__':
    # find_compromised_domains(pcap = ["../logs/2021-09-01-TA551-BazarLoader-with-Trickbot.pcap"])
    # find_compromised_domains(evtx = ["../logs/DE_RDP_Tunnel_5156.evtx"])
    # find_compromised_domains(xml = ["../logs/example_log.xml"],
    #                          json = ["../logs/example_log.json"],
    #                          txt = ["../logs/example_log.txt"])
    find_compromised_domains(pcap = ["../logs/2021-09-01-TA551-BazarLoader-with-Trickbot.pcap"],
                             evtx = ["../logs/DE_RDP_Tunnel_5156.evtx"],
                             xml = ["../logs/example_log.xml"],
                             json = ["../logs/example_log.json"],
                             txt = ["../logs/example_log.txt"])
    # find_compromised_ip(pcap = ["../logs/2021-09-01-TA551-BazarLoader-with-Trickbot.pcap"])
    # find_compromised_ip(evtx = ["../logs/DE_RDP_Tunnel_5156.evtx"])
    # find_compromised_ip(xml = ["../logs/example_log.xml"],
    #                          json = ["../logs/example_log.json"],
    #                          txt = ["../logs/example_log.txt"])
    find_compromised_ip(pcap = ["../logs/2021-09-01-TA551-BazarLoader-with-Trickbot.pcap"],
                        evtx = ["../logs/DE_RDP_Tunnel_5156.evtx"],
                        xml = ["../logs/example_log.xml"],
                        json = ["../logs/example_log.json"],
                        txt = ["../logs/example_log.txt"])
