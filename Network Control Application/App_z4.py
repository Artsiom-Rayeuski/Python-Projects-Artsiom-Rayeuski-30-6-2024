import csv
import sys
import networkx as nx
import json
import requests


class Done(Exception):
    pass


def check_host(host):
    while True:
        try:
            for j in hosts:
                if host in j:
                    raise Done
                else:
                    pass
            print("A host ", host, " does not exist")
            host = input("Enter city from where you want to send data: ")
        except Done:
            print("Host is exist in our system")
            break
    return host


def json_creator(path, hosts, switches):
    ip_from = ""
    ip_to = ""
    flow_json = {"flows": []}
    for i in hosts:
        if path[0] in i:
            ip_to = "10.0.0." + i[1] + "/32"
            port = i[3]
            device_id = "of:00000000000000" + i[2]
            flow = {
                "priority": 1,
                "timeout": 0,
                "isPermanent": True,
                "deviceId": device_id,
                "treatment": {"instructions": [{"type": "OUTPUT", "port": port}]},
                "selector": {"criteria": [{"type": "ETH_TYPE", "ethType": "0x0800"},
                                          {"type": "IPV4_DST", "ip": ip_to}]}
            }
            flow_json["flows"].append(flow.copy())
            # print(ip_to)
        if path[len(path)-1] in i:
            ip_from = "10.0.0." + i[1] + "/32"
            port = i[3]
            device_id = "of:00000000000000" + i[2]
            flow = {
                "priority": 1,
                "timeout": 0,
                "isPermanent": True,
                "deviceId": device_id,
                "treatment": {"instructions": [{"type": "OUTPUT", "port": port}]},
                "selector": {"criteria": [{"type": "ETH_TYPE", "ethType": "0x0800"},
                                          {"type": "IPV4_DST", "ip": ip_from}]}
            }
            flow_json["flows"].append(flow.copy())
            # print(ip_from)
        else:
            pass
    count = 0
    while count < len(path) - 1:
        for i in switches:
            if path[count] in i and path[count + 1] in i:
                temp = 0
                if path[count] != i[0]:
                    temp = 1
                port_to = i[3+temp]
                port_from = i[4-temp]
                device_id_to = "of:00000000000000" + i[7+temp]
                device_id_from = "of:00000000000000" + i[8-temp]
                flow_to = {
                    "priority": 1,
                    "timeout": 0,
                    "isPermanent": True,
                    "deviceId": device_id_to,
                    "treatment": {"instructions": [{"type": "OUTPUT", "port": port_to}]},
                    "selector": {"criteria": [{"type": "ETH_TYPE", "ethType": "0x0800"},
                                              {"type": "IPV4_DST", "ip": ip_from}]}
                }
                flow_from = {
                    "priority": 1,
                    "timeout": 0,
                    "isPermanent": True,
                    "deviceId": device_id_from,
                    "treatment": {"instructions": [{"type": "OUTPUT", "port": port_from}]},
                    "selector": {"criteria": [{"type": "ETH_TYPE", "ethType": "0x0800"},
                                              {"type": "IPV4_DST", "ip": ip_to}]}
                }
                flow_json["flows"].append(flow_to.copy())
                flow_json["flows"].append(flow_from.copy())
                break
            else:
                pass
        count += 1
    return flow_json


def path_chooser(G, source, target):
    path_temp = []
    i = 0
    while i < len(source):
        path_temp.append(nx.dijkstra_path(G, source[i], target[i]))
        # print(path_temp[i])
        i += 1

    j = 0
    while j < len(source) - 1:
        if path_temp[0][j] in path_temp[1] and path_temp[0][j + 1] in path_temp[1]:
            G.remove_edge(path_temp[0][j], path_temp[0][j + 1])
            # print(G.has_edge(path_temp[0][i], path_temp[0][i+1]))
            if nx.has_path(G, path_temp[1][0], path_temp[1][len(source)-1]):
                del path_temp[1]
                path_temp.append(nx.dijkstra_path(G, source[1], target[1]))
                # print(path_temp[1])
            else:
                pass
        j += 1

    return path_temp.copy()


hosts = []
switches = []
row_count = 0

try:
    f1 = open("Hosts.csv", 'r')
    f2 = open("Switch.csv", 'r')
except OSError:
    print("Could not open/read file:", "Hosts.csv")
    sys.exit()

with f1:
    hosts_csv = csv.reader(f1, delimiter=';')
    for row in hosts_csv:
        hosts.append(row)

with f2:
    switch_csv = csv.reader(f2, delimiter=';')
    for row in switch_csv:
        switches.append(row)
        row_count += 1

G = nx.Graph()

row = 1
while row < row_count:
    G.add_edge(switches[row][0], switches[row][1], weight=int(switches[row][2]))
    row += 1

counter = int(input("How much connections you want to establish: "))

i = 0
source = []
target = []
data_stream_size = []

while i < counter:
    source.append(check_host(input("Host from where you want to send data: ")))
    target.append(check_host(input("Host to where you want to send data: ")))
    data_stream_size.append(input("Data stream size: "))
    i += 1


# source = ["Leeds", "Edinburgh"]
# target = ["London", "Birmingham"]

path = path_chooser(G, source, target).copy()

i = 0
while i < len(source):
    print(str(i+1) + " path between hosts:  ", path[i])
    data = json_creator(path[i], hosts, switches)
    with open("cfg_" + str(i) + ".json", "w") as outfile:
        json.dump(data, outfile)
        outfile.close()
    i += 1


i = 0
response = []
while i < counter:
    with open("cfg_" + str(i) + ".json", "r") as outfile:
        r = requests.post("http://192.168.100.4:8181/onos/v1/flows/", json=json.load(outfile), auth=("onos", "rocks"))
        response.append(r.json())
        i += 1
        print(r.status_code)

if input("Do u want to delete flows(write: yes): ") == "yes":
    for i in response:
        for j in i["flows"]:
            r = requests.delete("http://192.168.100.4:8181/onos/v1/flows/" + j["deviceId"] + "/" + j["flowId"],
                                auth=("onos", "rocks"))
