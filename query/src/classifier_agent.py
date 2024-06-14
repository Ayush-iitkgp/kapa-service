from org.models import Project
from query.src.classifier import DummyClassifier


class ClassifierAgent:
    """
    class for doing classification of the question
    """

    def __init__(self, project: Project):
        self.project = project
        self.possible_labels = list(project.labels)

    def classify_question(self, question: str) -> str:
        """
        Generate a label to a question based on the classifier
        """

        # Perform classification
        classifier = DummyClassifier(project=self.project)
        return classifier.classify_question(question, self.possible_labels)
