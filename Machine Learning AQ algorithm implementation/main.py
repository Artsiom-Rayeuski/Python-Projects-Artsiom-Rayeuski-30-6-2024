"""
File: main.py
Authors: Artsiom Rayeuski, Jan Wisniewski
Date: 21/01/2024
Description: Main script for testing and showing generated rules.
"""

from data_grabber import data_grabber
from data_segregator import data_segregator
from sequential_covering_algorithm import sequential_covering_algorithm


if __name__ == '__main__':

    # Load data and class labels using the data_grabber module
    data, classes, custom_indexes, unique_values = data_grabber(1)

    # Segregate the data into training and testing sets
    data_train, data_test, classes_train, classes_test = data_segregator(data, classes, 0.5)

    # Apply the sequential covering algorithm to generate a ruleset
    ruleset = sequential_covering_algorithm(data, classes, unique_values)

    # Print the generated rules
    for rule in ruleset:
        print(rule)
