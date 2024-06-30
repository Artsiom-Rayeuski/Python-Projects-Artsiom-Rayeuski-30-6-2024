"""
File: sequential_covering_algorithm.py
Authors: Artsiom Rayeuski, Jan Wisniewski
Date: 21/01/2024
Description: Implements the Sequential Covering Algorithm for rule generation.
"""

from aq import aq
from Rule import Rule


def sequential_covering_algorithm(data, classifiers, unique_values):
    """
    Generates a set of classification rules using the Sequential Covering Algorithm.

    Parameters:
    - data (list): List of instances.
    - classifiers (list): List of corresponding classes.
    - unique_values (list): Unique values for each attribute in the dataset.

    Returns:
    - list: A set of classification rules.
    """
    # Initialize an empty list to store the generated rules
    ruleset_R = []

    # Make a copy of the input data to work with
    data_R = data
    while len(data_R) != 0:
        # Generate a rule using the AQ algorithm
        rule = aq(data_R, classifiers, unique_values)

        ruleset_R.append(rule)

        # Initialize new lists for instances and corresponding classes
        new_list = []
        new_class = []

        for x in data_R:
            remove = True

            # Check if the instance satisfies the conditions of the generated rule
            for i in range(len(x)):
                if not x[i] in rule.my_complex[i]:
                    remove = False
                    break

            # If the instance does not satisfy the rule, add it to the new list
            if not remove:
                new_list.append(x)
                new_class.append(classifiers[data_R.index(x)])

        # Update the classifiers and data set for the next iteration
        classifiers = new_class
        data_R = new_list

    # Return the final set of generated rules
    return ruleset_R
