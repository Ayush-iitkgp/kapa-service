import random
import time
from typing import List

from org.models import Project


class DummyClassifier:
    """
    Feel free to rewrite this code as needed, if that will suit your code structure better.
    However, you do not need to make any changes to this class. You do not have to implement
    an actual classifier.
    """

    def __init__(self, project: Project):
        self.project = project

    def classify_question(self, question: str, possible_labels: List[str]) -> str:
        """
        Assign a label from a list of possible labels to an question.

        This is an expensive operation it takes 2 seconds. (I/O bound)
        """
        time.sleep(2)  # Classification is not instant

        if not possible_labels:
            raise ValueError("The list of possible labels is empty")

        # We just return a random label
        return random.choice(possible_labels)
