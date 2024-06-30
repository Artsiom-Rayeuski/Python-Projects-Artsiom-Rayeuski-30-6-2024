"""
File: data_segregator.py
Authors: Artsiom Rayeuski, Jan Wisniewski
Date: 21/01/2024
Description: Module for segregating data into training and testing sets.
"""

import data_grabber
from sklearn.model_selection import train_test_split


def data_segregator(features, labels, percentage):
    """
    Segregates data randomly into training and testing sets.

    Parameters:
    - features (list): List of feature values.
    - labels (list): List of corresponding labels.
    - percentage (float): Percentage of the data to be used for testing.

    Returns:
    - tuple: Features and labels for training and testing sets.
    """
    # Define the percentage for the test set
    test_size = percentage  # x % of the data will be used for testing

    # Use train_test_split to split the data
    # random_state: int, RandomState instance or None, default=None
    features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels, test_size=test_size, random_state=None
    )

    # Now features_train and labels_train are the training sets, and features_test and labels_test are the testing sets
    return features_train, features_test, labels_train, labels_test
