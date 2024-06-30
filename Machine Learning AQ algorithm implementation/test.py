"""
File: test.py
Authors: Artsiom Rayeuski, Jan Wisniewski
Date: 21/01/2024
Description: Script for testing the aq using a dataset, evaluating its performance, and presenting results.
"""

from data_grabber import data_grabber
from data_segregator import data_segregator
from sequential_covering_algorithm import sequential_covering_algorithm
import statistics


def classify_data(ruleset_to_test, test_data):
    """
    Classifies the given test data using the provided ruleset.

    Parameters:
    - ruleset_to_test (list): List of classification rules.
    - test_data (list): List of instances to be classified.

    Returns:
    - list: Predicted classes for the test data.
    """
    predictions = []
    for data_point in test_data:
        predicted_class = None
        # Check each rule in the ruleset
        for rule in ruleset_to_test:
            not_in_rule = False

            # Iterate through each condition set in the rule
            for idx, condition_set in enumerate(rule.my_complex):
                if not data_point[idx] in condition_set:
                    not_in_rule = True
                    break

            # If the data point satisfies the rule, assign the predicted class
            if not not_in_rule:
                predicted_class = rule.classifier
                break

        # Append the predicted class to the list of predictions
        predictions.append(predicted_class)

    return predictions


def evaluate_ruleset(ruleset_to_test, test_data, test_classes, unique_classes):
    """
    Evaluates the performance of the provided ruleset on the test data.

    Parameters:
    - ruleset_to_test (list): List of classification rules.
    - test_data (list): List of instances to be classified.
    - test_classes (list): List of actual classes corresponding to the test data.
    - unique_classes (list): List of unique classes in the dataset.

    Returns:
    - tuple: Precision value and error matrix.
    """
    correct_class = 0
    error_matrix = {}

    for unique_class in unique_classes:
        # [True Positive, False Positive, False Negative, True Negative]
        error_matrix[unique_class] = [0, 0, 0, 0]

    predictions = classify_data(ruleset_to_test, test_data)

    for predicted_class, actual_class in zip(predictions, test_classes):
        # Check if the predicted class matches the actual class
        if predicted_class is not None and predicted_class == actual_class:
            correct_class += 1
            error_matrix[actual_class][0] += 1
        elif predicted_class != actual_class:
            error_matrix[actual_class][2] += 1
            error_matrix[predicted_class][1] += 1

    # Calculate the True Negatives (TN) for each unique clas
    for unique_class in unique_classes:
        error_matrix[unique_class][3] = len(test_classes) - sum(error_matrix[unique_class])

    # Calculate precision as the ratio of correct classifications to the total number of instances
    precision = correct_class / len(test_classes)

    return precision, error_matrix


if __name__ == '__main__':
    # Initialize variables for storing results
    accuracy = []
    error_matrix_full = []
    ruleset = []
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    # Grab dataset and unique classes
    data, classes, custom_indexes, unique_values = data_grabber(1)
    unique_classes_full = list(set(classes))

    for i in range(30):

        # Split data into training and testing sets
        data_train, data_test, classes_train, classes_test = data_segregator(data, classes, 0.5)

        # Apply the sequential covering algorithm to generate a ruleset
        ruleset = sequential_covering_algorithm(data_train, classes_train, unique_values)

        # Evaluate the performance of the ruleset on the testing set
        value, error_matrix_value = (
            evaluate_ruleset(ruleset, data_test, classes_test, unique_classes_full)
        )

        # Store the results for later analysis
        error_matrix_full.append(error_matrix_value)
        accuracy.append(value)

    # Calculate metrics for each unique class
    for unique_class in unique_classes_full:
        print(f"    ========= {unique_class} =========")
        for matrix in error_matrix_full:
            TP += matrix[unique_class][0]
            FP += matrix[unique_class][1]
            FN += matrix[unique_class][2]
            TN += matrix[unique_class][3]
        TP = TP / len(error_matrix_full)
        FP = FP / len(error_matrix_full)
        FN = FN / len(error_matrix_full)
        TN = TN / len(error_matrix_full)
        TPR = TP / (TP + FN)
        TNR = TN / (TN + FP)
        PPV = TP / (TP + FP)
        ACC = (TP + TN) / (TP + TN + FP + FN)
        F1 = 2 * TP / (2 * TP + FP + FN)

        # Format the values as per your specified format
        formatted_TP = "{:,.2f}".format(TP).replace('.', ',')
        formatted_FP = "{:,.2f}".format(FP).replace('.', ',')
        formatted_FN = "{:,.2f}".format(FN).replace('.', ',')
        formatted_TN = "{:,.2f}".format(TN).replace('.', ',')
        formatted_TPR = "{:,.2f}".format(TPR).replace('.', ',')
        formatted_TNR = "{:,.2f}".format(TNR).replace('.', ',')
        formatted_PPV = "{:,.2f}".format(PPV).replace('.', ',')
        formatted_ACC = "{:,.2f}".format(ACC).replace('.', ',')
        formatted_F1 = "{:,.2f}".format(F1).replace('.', ',')

        print(f"        TP = {formatted_TP} | FN = {formatted_FN} | FP = {formatted_FP} | TN = {formatted_TN}")
        print(f"        TPR = {formatted_TPR}")
        print(f"        TNR = {formatted_TNR}")
        print(f"        PPV = {formatted_PPV}")
        print(f"        ACC = {formatted_ACC}")
        print(f"        F1 = {formatted_F1}")

    # Calculate and display overall accuracy metrics
    print()
    mean_accuracy = ("{:,.2f}"
                     .format(sum(accuracy)/len(accuracy))
                     .replace('.', ','))
    print(f"Accuracy: {mean_accuracy}")
    max_accuracy = ("{:,.2f}"
                    .format(max(accuracy)).replace('.', ','))
    print(f"The best result: {max_accuracy}")
    min_accuracy = ("{:,.2f}"
                    .format(min(accuracy)).replace('.', ','))
    print(f"The worst result: {min_accuracy}")
    standard_deviation = ("{:,.2f}"
                          .format(statistics.stdev(accuracy))
                          .replace('.', ','))
    print(f"Standard deviation: {standard_deviation}")
