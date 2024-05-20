import logging
import random
from typing import List

from query.src.types import LLMGeneration, Message

logger = logging.getLogger(__name__)

import time


class LLMClient:
    """
    class for making calls to an LLM
    """

    answers = [
        LLMGeneration(
            text="HTTPS is HTTP with encryption. HTTPS uses TLS (SSL) to encrypt data between the client and server, making it more secure.",
            tokens=100,
        ),
        LLMGeneration(
            text="REST (Representational State Transfer) API is a set of rules for creating web services that allow communication between client and server over HTTP.",
            tokens=50,
        ),
        LLMGeneration(
            text="A DNS (Domain Name System) server translates domain names (like www.example.com) into IP addresses so browsers can load internet resources.",
            tokens=100,
        ),
        LLMGeneration(
            text="A virtual machine (VM) is a software emulation of a physical computer, allowing multiple OS to run on a single physical machine.",
            tokens=110,
        ),
        LLMGeneration(
            text="A container in Docker is a lightweight, standalone, executable package that includes everything needed to run a piece of software, including the code, runtime, libraries, and settings.",
            tokens=130,
        ),
        LLMGeneration(
            text="Git is a distributed version control system that tracks changes in source code during software development, allowing multiple developers to work on a project simultaneously.",
            tokens=110,
        ),
        LLMGeneration(
            text="A compiler translates high-level code into machine code before execution, while an interpreter translates and executes code line by line.",
            tokens=90,
        ),
        LLMGeneration(
            text="A microservice is an architectural style that structures an application as a collection of loosely coupled, independently deployable services.",
            tokens=100,
        ),
        LLMGeneration(
            text="An IP address is a unique string of numbers separated by periods or colons that identifies each computer using the Internet Protocol to communicate over a network.",
            tokens=105,
        ),
        LLMGeneration(
            text="Machine learning is a subset of artificial intelligence that uses algorithms and statistical models to enable computers to improve at tasks with experience.",
            tokens=102,
        ),
        LLMGeneration(
            text="A firewall is used to protect a network by controlling incoming and outgoing network traffic based on predetermined security rules.",
            tokens=99,
        ),
    ]

    def chat_completion(
        self,
        messages: List[Message],
    ) -> LLMGeneration:
        """
        In the normal system this sends the messages to an LLM to generate
        text. For simplicity of this excercise it just returns some random technical descriptons.

        You do not need to make any changes here.
        """
        time.sleep(1)
        return random.choice(self.answers)
