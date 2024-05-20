import uuid
from typing import List, TypedDict

from org.models import Project
from query.models import QuestionAnswer, Thread
from query.src.llm_client import LLMClient
from query.src.retriever import Retriever
from query.src.types import Chunk, Message, RAGResult


class RAGAgent:
    """
    Read only class for doing semantic retrieval
    """

    def __init__(self, project: Project):
        self.project = project
        self.llm_client = LLMClient()

    def generate_answer(self, question: str) -> RAGResult:
        """
        Generate an answer to a first question based on RAG
        """

        # Perform retrieval
        retriever = Retriever(project=self.project)
        relevant_chunks = retriever.get_relevant_chunks(question=question)

        # Construct messages
        messages = self._construct_chat_messages_first_question(
            question, relevant_chunks
        )

        # Generate answers
        result = self.llm_client.chat_completion(messages=messages)

        # Persist the answer in a new thread
        thread = Thread.objects.create(project=self.project)
        question_answer = QuestionAnswer.objects.create(
            thread=thread,
            question=question,
            answer=result["text"],
        )

        return RAGResult(
            question=question_answer.question,
            answer=question_answer.answer,
            question_answer_id=question_answer.id,
            thread_id=thread.id,
        )

    def generate_follow_up_answer(self, question: str, thread: Thread) -> RAGResult:
        """
        Generate an answer to follow up question based on RAG
        """

        # Perform retrieval
        retriever = Retriever(project=self.project)
        relevant_chunks = retriever.get_relevant_chunks(question=question)

        # Construct messages with chat history
        messages = self._construct_chat_messages_follow_up_question(
            thread, question, relevant_chunks
        )

        # Generate answer
        result = self.llm_client.chat_completion(messages=messages)

        # Persist the answer in an existing thread
        question_answer = QuestionAnswer.objects.create(
            thread=thread,
            question=question,
            answer=result["text"],
        )

        return RAGResult(
            question=question_answer.question,
            answer=question_answer.answer,
            question_answer_id=question_answer.id,
            thread_id=thread.id,
        )

    def _construct_chat_messages_first_question(
        self, query: str, relevant_chunks: List[Chunk]
    ) -> List[Message]:
        """
        Construct the prompt to be sent to an LLM for a first question
        in a 'Thread'
        """
        return [
            Message(role="system", content="You are a helpful programming expert."),
            Message(
                role="user",
                content="Please answer a user question based on the following knowledge sources.",
            ),
            [
                Message(role="user", content=chunk["content"])
                for chunk in relevant_chunks
            ],
            Message(role="user", content=f"user question: {query}"),
        ]

    def _construct_chat_messages_follow_up_question(
        self, thread: Thread, query: str, relevant_chunks: List[Chunk]
    ) -> List[Message]:
        """
        Construct the prompt to be sent to an LLM for a follow up question
        in a 'Thread'
        """

        previous_question_answers = QuestionAnswer.objects.filter(
            thread_id=thread.id
        ).order_by("created_at")

        conversation_history: List[Message] = []
        for question_answer in previous_question_answers:
            conversation_history.append(
                Message(role="user", content=question_answer.question)
            )
            conversation_history.append(
                Message(role="assistant", content=question_answer.answer)
            )

        return [
            Message(role="system", content="You are a helpful programming expert."),
            Message(
                role="user",
                content="Please answer a user follow up question based on the following knowledge sources.",
            ),
            [
                Message(role="user", content=chunk["content"])
                for chunk in relevant_chunks
            ],
            Message(role="user", content=f"Here is the conversation history:"),
            conversation_history,
            Message(role="user", content=f"New user question: {query}"),
        ]
