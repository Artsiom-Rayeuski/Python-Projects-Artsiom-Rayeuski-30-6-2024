# Network Control Application

## Overview

This Python application configures network resources using the ONOS controller and Mininet network emulator. It reads network topology from CSV files, computes optimal paths for data streams between hosts, and generates configuration files in JSON format to be used by ONOS.

## Features

- **Path Calculation:** Uses Dijkstra's algorithm to compute the shortest paths between specified hosts.
- **Dynamic Configuration:** Generates flow configuration files based on network topology and user inputs.
- **ONOS Integration:** Interacts with the ONOS controller via its REST API to apply and manage network configurations.


The application will calculate the paths, generate the configuration files, and apply them to the ONOS controller.
