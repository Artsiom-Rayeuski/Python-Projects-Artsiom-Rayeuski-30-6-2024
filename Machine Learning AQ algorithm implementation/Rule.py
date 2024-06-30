"""
File: Rule.py
Authors: Artsiom Rayeuski, Jan Wisniewski
Date: 21/01/2024
Description: Defines the Rule class for representing a classification rule.

The Rule class encapsulates a classification rule with a condition (my_complex) and a corresponding classifier.

Functions:
- __init__(self, my_complex, classifier): Initializes a Rule instance with the given condition and classifier.
- __repr__(self): Returns a string representation of the Rule instance.
- __str__(self): Returns a human-readable string representation of the Rule instance.

"""


class Rule:
    def __init__(self, my_complex, classifier):
        self.my_complex = my_complex
        self.classifier = classifier

    def __repr__(self):
        return f"Rule(condition='{self.my_complex}', classifier='{self.classifier}')"

    def __str__(self):
        return f"If {self.my_complex} then {self.classifier}"
