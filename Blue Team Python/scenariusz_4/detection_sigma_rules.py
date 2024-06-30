import json
import os
import yaml
import click
from Evtx.Evtx import Evtx
import xmltodict

FILE = 1
DIRECTORY = 2
NEITHER = 3
DOES_NOT_EXIST = 4


def check_path_type(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            print(f"{path} is a file.")
            return FILE
        elif os.path.isdir(path):
            print(f"{path} is a directory.")
            return DIRECTORY
        else:
            exit(f"{path} exists, but is neither a file nor a directory.")
    else:
        exit(f"{path} does not exist.")


def read_logs_from_evtx(evtx_path):
    print("Reading logs from: " + click.format_filename(evtx_path))
    result = check_path_type(evtx_path)
    if result == FILE:
        try:
            with Evtx(evtx_path) as parser:
                return parser.records()

        except Exception as e:
            exit(f"Evtx reading failed: {e}")
    else:
        exit(print(f"{evtx_path} is not a file."))


def read_yaml_file(yaml_file_path):
    try:
        with open(yaml_file_path, 'r') as file:
            data_dict = yaml.safe_load(file)
        print(f"Reading successful: YAML file '{yaml_file_path}' is valid.")
        return data_dict

    except yaml.YAMLError as e:
        print(f"Reading failed: {e}")
        return None


def apply_sigma_rule(event_data, sigma_rule):
    # Check if the log entry matches the Sigma rule
    print(sigma_rule['detection'])
    if all(selection_check(event_data, sigma_rule[key]) for key in sigma_rule['detection']):
        return True
    return False


def selection_check(event_data, selection):
    if isinstance(selection, list):
        # For "all" conditions
        return all(selection_check(event_data, sub_selection) for sub_selection in selection)
    elif isinstance(selection, dict):
        # For "any" conditions
        return any(selection_check(event_data, sub_selection) for sub_selection in selection)
    else:
        # Perform the specific check based on the selection condition
        field, operator, value = selection.split('|')
        field_value = event_data.get(field, '')

        if operator == 'contains':
            return value.lower() in field_value.lower()
        elif operator == 'endswith':
            return any(field_value.lower().endswith(suffix.lower()) for suffix in value)
        else:
            return False  # Add more conditions as needed


def detect_malicious_activity(logs, sigma_rule_path):
    sigma_rule = json.loads(json.dumps(read_yaml_file(sigma_rule_path)))
    print(sigma_rule)
    with Evtx(logs) as parser:
        for log in parser.records():
            event_data = log.xml()
            dict_data = xmltodict.parse(event_data)
            json_data = json.dumps(dict_data, indent=2)
            json_log = json.loads(json_data)
            print(json.dumps(json_log,indent=4))
        # Apply Sigma rule to check for malicious activity
            if apply_sigma_rule(json_log, sigma_rule):
                print("Malicious activity detected:", json.dumps(json_log,indent=4))


def analyze(evtx_logs_path, sigma_rule_yaml_path):
    global rules
    evtx_logs = read_logs_from_evtx(evtx_logs_path)
    yaml_path_type = check_path_type(sigma_rule_yaml_path)
    if yaml_path_type == FILE:
        print("Ruleset: " + click.format_filename(sigma_rule_yaml_path))
        detect_malicious_activity(evtx_logs_path, sigma_rule_yaml_path)
    elif yaml_path_type == DIRECTORY:
        files = [f for f in os.listdir(sigma_rule_yaml_path) if os.path.isfile(os.path.join(sigma_rule_yaml_path, f))]
        for file in files:
            print("Rule file: " + click.format_filename(file))
            detect_malicious_activity(evtx_logs_path, file)


if __name__ == "__main__":
    print("a")
