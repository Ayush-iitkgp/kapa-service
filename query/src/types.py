import uuid
from typing import TypedDict


class Chunk(TypedDict):

    """
    Represents a retrieved piece of a document
    """

    id: str
    content: str


class RAGResult(TypedDict):
    """
    Result of a retrieval augmented generation
    """

    question: str
    answer: str
    question_answer_id: uuid.UUID
    thread_id: uuid.UUID


class Message(TypedDict):
    """
    Represents a message to be sent to an LLM
    """

    role: str
    content: str


class LLMGeneration(TypedDict):
    """
    Represents the output of an LLM
    """

    text: str
    tokens: int


class Label(TypedDict):
    """
    Represents a label that can be assigned to an entity
    """

    id: uuid.UUID
    title: str
    description: str
