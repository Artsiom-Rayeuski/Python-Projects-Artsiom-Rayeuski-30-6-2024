"""
GroupId default Databases = 20
GroupId default Applications = 19
GroupId default Zabbix servers = 4
MySQL by Zabbix agent have snmp_discovery_rule_id = 10316
Internal groupId = 13
UserRole snmp_discovery_rule_id = 1
Templates/Applications is in group 12
Templates/Databases is in group 13
Telegram media has id  16
Email media has id  1
SMS media has id  3
Email (HTML) media has id  4
Gmail media has id  34
Gmail relay media has id  35
Office 365 media has id  36
Office 365 relay media has id  37
Telegram media has id  16
{__IP__}/{__MASK__}
"""
import json
import sys
import ifaddr
from pyzabbix import ZabbixAPI, ZabbixAPIException


def mysql_auto_registration(zapi):
    try:
        with open("json/MySQL_auto_registration.json") as file:
            data = json.load(file)["params"]
        action = zapi.action.create(data)
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added MySQL auto registration with itemid {}".format(action["actionids"][0]))


def create_client_user(zapi):
    try:
        with open("json/create_client_user.json") as file:
            data = json.load(file)["params"]
        action = zapi.user.create(data)
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added user 'user' with userid {}".format(action["userids"][0]))


def create_user_group(zapi):
    try:
        with open("json/create_user_group.json") as file:
            data = json.load(file)["params"]
        action = zapi.usergroup.create(data)
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added SNMP and MySQL monitor group with groupid {}".format(action["usrgrpids"][0]))


def get_eth0_ip_and_mask():
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        if adapter.nice_name == 'eth0':
            for ip in adapter.ips:
                if ip.is_IPv4:
                    ip_address_to_process = ip.ip
                    segments = ip_address_to_process.split(".")
                    ip_address = segments[0] + "." + segments[1] + "." + segments[2] + ".0"
                    mask = ip.network_prefix
                    if mask < 24:
                        cidr_mask = str(24)
                    else:
                        cidr_mask = str(mask)

                    return ip_address, cidr_mask
    return None, None


def create_discovery_rule(zapi, ip, mask):
    try:
        with open("json/discover_rule_snmp_agent.json") as file:
            json_data = json.load(file)
            data = json_data["params"]
            data = json.dumps(data)  # Convert the dictionary to a string
            data = data.replace("{__IP__}", ip).replace("{__MASK__}", mask)
            # Convert back to a dictionary before calling the create method
            action = zapi.drule.create(json.loads(data))
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Created discovery rule for finding SNMP with druleid {}".format(action["druleids"][0]))
    return action["druleids"][0]


def create_discovery_action(zapi, snmp_discovery_rule_id):
    try:
        with open("json/SNMP_discovery_action.json") as file:
            json_data = json.load(file)
            data = json_data["params"]
            data = json.dumps(data)  # Convert the dictionary to a string
            data = data.replace('"{__ID__}"', str(snmp_discovery_rule_id))
        action = zapi.action.create(json.loads(data))
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added discovery action for finding SNMP with itemid {}".format(action["actionids"][0]))


def enable_telegram_media(zapi):
    try:
        with open("json/enable_telegram_media.json") as file:
            data = json.load(file)["params"]
        action = zapi.mediatype.update(data)
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Enable telegram media {}".format(action["mediatypeids"][0]))


def set_trigger_action(zapi):
    try:
        with open("json/add_trigger_to_send_problems_via_telegram.json") as file:
            data = json.load(file)["params"]
        action = zapi.action.create(data)
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added trigger action with itemid {}".format(action["actionids"][0]))


def main():
    zapi = ZabbixAPI("http://localhost/zabbix")
    zapi.login("Admin", "zabbix")
    print("Connected to Zabbix API Version %s" % zapi.api_version())
    # For debugging
    # for h in zapi.mediatype.get():
    #    print(h["name"] + " media has id  " + h["mediatypeid"])

    # Enabling telegram media
    enable_telegram_media(zapi)

    # Creating user for client
    create_client_user(zapi)
    create_user_group(zapi)

    # Trigger for actions
    set_trigger_action(zapi)

    # Mysql servers with Zabbix agent auto registration
    mysql_auto_registration(zapi)

    # SNMP api configuration
    ip, mask = get_eth0_ip_and_mask()
    drule_id = create_discovery_rule(zapi, ip, mask)
    create_discovery_action(zapi, drule_id)


if __name__ == "__main__":
    main()
