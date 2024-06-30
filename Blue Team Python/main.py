import os
import inspect
import importlib
import click
import requests
import logging
import json
from datetime import datetime
from scenariusz_1.scenariusz_1 import PCAPAnalyzer
import scenariusz_2.scenariusz_2
import scenariusz_3.detection_rules
import scenariusz_3.update_compromised_lists
import scenariusz_4.detection_sigma_rules


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
@click.group()
@click.option("--log-file", type=click.Path(), default="edr_system.log", help="Path to the log file")
def cli(log_file):
    """Threat Analyzer"""
    # Configure the logging module to write to a file
    logging.basicConfig(filename = log_file, level = logging.INFO, format = "%(asctime)s [%(levelname)s]: %(message)s")
    pass


@cli.command()
@click.argument("pcap_file", type=click.Path(exists=True), required=True)
@click.option("--apply-filter", is_flag=True, help="Apply BPF filter to packets")
@click.option("--bpf-filter", type=str, help="BPF filter string")
def pcap_analyzer(pcap_file, apply_filter, bpf_filter):
    analyzer = PCAPAnalyzer()
    analyzer.analyze_pcap_file(pcap_file, apply_filter, bpf_filter)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True), required=True)
@click.option("--use-grep", "-g", is_flag=True, help="Use grep for analysis")
@click.option("--regex", "-re", type=str, help="Regular expression for analysis")
def text_log_analyzer(input_file, use_grep, regex):
    scenariusz_2.scenariusz_2.offline_file_analysis(input_file, regex, use_grep)


@cli.command()
@click.argument("input_files", type=click.Path(exists=True), required=False, nargs=-1)
@click.option("-r", "--rule", "rules", multiple=True, type=str, default=[], help="Specify a rule(s) for files")
@click.option("--all", "all_rules", is_flag=True, default=False, help="Use all existing rules")
@click.option("--update-compr-lists", "update_compromised_lists", is_flag=True, default=False,
              help="Update list of compromised domain names and ip addresses(require internet access)")
@click.pass_context
def python_rules(ctx, rules, all_rules, input_files, update_compromised_lists):
    # If no option is chosen, print the help message
    if not any(ctx.params[option] for option in ['rules', 'all_rules', 'update_compromised_lists']):
        print("Choose one of the options")
        click.echo(ctx.get_help())
    elif input_files is None:
        print("No files were chosen")
    else:
        # Create kwargs from input files
        kwargs = {'pcap': [], 'evtx': [], 'json': [], 'txt': [], 'xml': []}
        for file in input_files:
            _, file_extension = os.path.splitext(file.lower())
            if file_extension == '.pcap':
                kwargs['pcap'].append(file)
            elif file_extension == '.evtx':
                kwargs['evtx'].append(file)
            elif file_extension == '.json':
                kwargs['json'].append(file)
            elif file_extension == '.txt':
                kwargs['txt'].append(file)
            elif file_extension == '.xml':
                kwargs['xml'].append(file)
            else:
                print(f"This file/file extension: {os.path.basename(file)} is not supported")
        # Getting rule names from detection_rules.py
        loader = importlib.machinery.SourceFileLoader('detection_rules.py', "scenariusz_3/detection_rules.py")
        module = loader.load_module()
        # Use inspect to find all functions in the module
        functions = inspect.getmembers(
            module,
            lambda x: inspect.isfunction(x) and inspect.getmodule(x) == module
        )
        # Extract function names
        function_names = [function[0] for function in functions]
        # print(function_names)

        def calling_detection_rules(rule):
            data = {}
            headers = {'Content-type': 'application/json'}
            if hasattr(module, rule) and callable(getattr(module, rule)):
                function = getattr(module, rule)
                result_action_alert, result_description = function(**kwargs)
                if result_description is None:
                    return None
                description_lines = result_description.splitlines()
                if result_action_alert == "local":
                    for line in description_lines:
                        logging.warning(line)
                elif result_action_alert == "remote":
                    try:
                        for line in description_lines:
                            logging.warning(line)
                            # Get the current timestamp
                            current_time = datetime.now()
                            # Format the timestamp
                            formatted_timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
                            data["timestamp"] = formatted_timestamp
                            data["description"] = line
                            data_json = json.dumps(data)
                            requests.post("http://127.0.0.1:5000/save_event", data = data_json, headers = headers)
                    except requests.exceptions.ConnectionError:
                        print("Remote action can not be done, because Remote Event Collector is off")
                        return None
            else:
                print(f"Rule: {rule} not found in file detection_rules.py")

        if all_rules:
            for rule in function_names:
                calling_detection_rules(rule)
        elif rules:
            for rule in rules:
                calling_detection_rules(rule)
        elif update_compromised_lists:
            scenariusz_3.update_compromised_lists.update_compromised_lists()


@cli.command()
@click.argument("input_file", type=click.Path(exists=True), required=True)
@click.option("--ruleset", "-r", "ruleset", type=click.Path(exists=True), required=True)
def sigma_rules(input_file, ruleset):
    scenariusz_4.detection_sigma_rules.analyze(input_file, ruleset)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cli()
    # print_hi('PyCharm')
    # scenariusz_3.update_compromised_lists.update_compromised_lists()

