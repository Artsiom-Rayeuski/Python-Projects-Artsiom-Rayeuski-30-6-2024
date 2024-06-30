# Blue Team Python

## Project Overview

This project involves developing a prototype tool in Python for the detection and analysis of cyber threats based on data from hosts and networks. The project is divided into several scenarios and tasks aimed at creating an EDR/XDR (Endpoint Detection and Response/Extended Detection and Response) system. The project requires a team of 4 members.

## Team Responsibilities

The team is responsible for:
- Monitoring networks and hosts.
- Managing data for detecting cyber threats.
- Developing a Python tool for integrated data management and threat detection.

## Data Sources

Data sources available for analysis include:
- PCAP files
- Text files (e.g., syslog) in various formats (txt, json, xml)
- Binary log files (EVTX)

## Tool Requirements

### EDR/XDR System Prototype

1. **System Skeleton Requirements**
   - **Cyber Threat Analyzer (CLI Application)**
     - Develop a CLI application in Python using the Click module.
     - The application should log actions to both CLI and a log file.
     - Allow specification of files/folders for analysis.
     - Supported file formats: txt, xml, json, pcap, evtx (converted to text formats).
     - Communicate with a Remote Event Collector via REST API.

   - **Remote Event Collector (CLI Application)**
     - Develop a CLI application in Python using the Click module.
     - Receive messages via REST API and log them to SQLite.
     - Operate in two modes: continuous message logging and historical data retrieval.

2. **Operational Scenarios**

   - **Scenario 1: Offline File Analysis - PCAP**
     - Display PCAP file contents.
     - Apply BPF filters (compatible with libpcap, tshark, pyshark, Wireshark, Scapy).

   - **Scenario 2: Offline File Analysis - TXT/Logs**
     - Use grep for regex operations on text files.
     - Apply Python regex operations on text files and EVTX files (converted to JSON/XML).

   - **Scenario 3: Python Language Rules**
     - Load event detection rules from a fixed file (detection-rules.py).
     - Each rule is a Python function and should be reloaded upon each invocation.
     - Output includes local or remote alerts and a textual description.

   - **Scenario 4: Universal Rule Format - SIGMA**
     - Integrate SIGMA rule detection using the Zircolite engine.
     - Apply and test SIGMA rules on datasets.

## Tools and Libraries

- Python modules: Click, msticpy, pandas, sqlite, scapy, pyshark, fastapi, uvicorn
- Separate Miniconda3 environment for the project.
- Operations using Python-wrapped system commands.
