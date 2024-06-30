"""
File: data_grabber.py
Authors: Artsiom Rayeuski, Jan Wisniewski
Date: 21/01/2024
Description: Script for grabbing and processing various datasets.
"""

import csv
from pathlib import Path


def data_grabber(option):
    """
    Grabs and processes datasets based on the specified option.

    Parameters:
    - option (int): An integer representing the dataset option to be processed.

    Returns:
    - tuple: A tuple containing features, targets, custom indexes, and unique values.
    """
    features = []
    targets = []
    custom_indexes = []
    unique_values = []

    if option == 1:
        # Dataset: Balance Scale
        custom_indexes = ["Class name", "Left weight", "Left distance", "Right weight", "Right distance"]
        file_path = Path("Data/balance+scale/balance-scale.data")
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[1:])
            targets.append(line[0])
        unique_values = get_unique_values(features)

    elif option == 2:
        # Dataset: Car Evaluation
        custom_indexes = ["Buying price", "Price of the maintenance", "Number of doors",
                          "Capacity in terms of persons to carry", "The size of luggage boot",
                          "Estimated safety of the car",
                          "Evaluation level (unacceptable, acceptable, good, very good)"]
        file_path = "Data/car+evaluation/car.data"
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[:-1])
            targets.append(line[-1])
        unique_values = get_unique_values(features)

    elif option == 3:
        # Dataset: Chess (King vs Rook vs King+Pawn)
        custom_indexes = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                          "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                          'White can win(won) or White cannot win(nowin)']
        file_path = Path("Data/chess+king+rook+vs+king+pawn/kr-vs-kp.data")
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[:-1])
            targets.append(line[-1])
        unique_values = get_unique_values(features)

    elif option == 4:
        # Dataset: Mushroom
        custom_indexes = ["Edible or poisonous", "Cap shape", "Cap surface", "Cap color", "Have bruises",
                          "Odor", "Gill attachment", "Gill spacing", "Gill size", "Gill color",
                          "Stalk shape", "Stalk root", "Stalk surface above ring", "Stalk surface below ring",
                          "Stalk color above ring", "Stalk color below ring", "Veil type", "Veil color",
                          "Ring number", "Ring type", "Spore print color", "Population", "Habitat"]
        file_path = Path("Data/mushroom/agaricus-lepiota.data")
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[1:])
            targets.append(line[0])
        unique_values = get_unique_values(features)

    elif option == 6:
        # Dataset: Zoo
        custom_indexes = []
        file_path = Path("Data/cn2_datasets/zoo.csv")
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[:-1])
            targets.append(line[-1])
        unique_values = get_unique_values(features)

    elif option == 8:
        # Dataset: Soybean
        custom_indexes = []
        file_path = Path("Data/cn2_datasets/soybean.csv")
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[:-1])
            targets.append(line[-1])
        unique_values = get_unique_values(features)

    elif option == 9:
        # Dataset: example
        custom_indexes = []
        file_path = Path("Data/example_test_data")
        data = read_data_from_file(file_path)
        for line in data:
            features.append(line[:-1])
            targets.append(line[-1])
        unique_values = get_unique_values(features)
    return features, targets, custom_indexes, unique_values


def read_data_from_file(file_path):
    """
    Reads data from a file and returns it as a list of lists.

    Parameters:
    - file_path (str): The path to the file containing the data.

    Returns:
    - list of lists: The data read from the file.
    """

    data = []

    with open(file_path, 'r') as file:
        # Use csv.reader with a delimiter and quote character
        csv_reader = csv.reader(file, delimiter = ',', quotechar = '"')

        for row in csv_reader:
            # Skip empty lines
            if row:
                data.append(row)

    return data


def print_data_as_table(data, index_names):
    """
    Adds indexes to data and prints it as a table.

    Parameters:
    - data (list of lists): The data to be printed.
    - index_names (list of str): The names of the indexes to be added.

    Returns:
    - None
    """
    # Validate that the number of index names matches the length of each row in the data
    if len(index_names) != len(data[0]):
        print(len(index_names), " ### ", len(data[0]))
        raise ValueError("Number of index names must match the length of each row in the data.")

    # Print header with index names
    header = ['Index'] + index_names
    print('|'.join(header))

    # Print a horizontal line to separate header and data
    print('-' * (sum(len(column) for column in header) + len(header) - 1))

    # Print data with indexes
    for i, row in enumerate(data):
        indexed_row = [str(i + 1)] + row
        print('|'.join(indexed_row))


def get_unique_values(all_values):
    """
    Transposes the data to iterate over columns and retrieves unique values for each column.

    Parameters:
    - all_values (list of lists): The data values.

    Returns:
    - list of lists: Unique values for each column.
    """
    # Transpose the data to iterate over columns
    transposed_data = list(zip(*all_values))

    # Get unique values for each column
    unique_values_per_column = [list(set(column)) for column in transposed_data]

    return unique_values_per_column
