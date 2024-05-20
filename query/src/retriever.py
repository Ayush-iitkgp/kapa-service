import random
from typing import List

from org.models import Project
from query.src.types import Chunk


class Retriever:
    """
    Read only class for doing semantic retrieval
    """

    documents = [
        Chunk(
            id=1,
            content="API Endpoint: The specific URL where an API receives requests from clients.",
        ),
        Chunk(
            id=2,
            content="CRUD Operations: Create, Read, Update, Delete - basic operations for data management.",
        ),
        Chunk(
            id=3,
            content="OAuth: An open standard for access delegation commonly used for token-based authentication.",
        ),
        Chunk(
            id=4,
            content="Load Balancer: A device that distributes network or application traffic across multiple servers.",
        ),
        Chunk(
            id=5,
            content="DNS (Domain Name System): Translates human-friendly domain names to IP addresses.",
        ),
        Chunk(
            id=6,
            content="Docker Container: A lightweight, standalone, and executable software package that includes everything needed to run a piece of software.",
        ),
        Chunk(
            id=7,
            content="Microservices: An architectural style that structures an application as a collection of loosely coupled services.",
        ),
        Chunk(
            id=8,
            content="RESTful API: An API that adheres to REST (Representational State Transfer) principles for communication.",
        ),
        Chunk(
            id=9,
            content="CI/CD Pipeline: Continuous Integration and Continuous Deployment - a process for automating the integration and deployment of code changes.",
        ),
        Chunk(
            id=10,
            content="SSL/TLS: Secure Sockets Layer/Transport Layer Security - protocols for establishing encrypted links between networked computers.",
        ),
        Chunk(
            id=11,
            content="Firewall: A network security device that monitors and filters incoming and outgoing network traffic.",
        ),
        Chunk(
            id=12,
            content="NoSQL Database: A non-relational database designed to handle large volumes of unstructured data.",
        ),
        Chunk(
            id=13,
            content="Machine Learning: A subset of AI that uses algorithms to enable computers to learn from data.",
        ),
        Chunk(
            id=14,
            content="WebSocket: A protocol for two-way communication between a client and server over a single, long-lived connection.",
        ),
        Chunk(
            id=15,
            content="Kubernetes: An open-source platform for managing containerized workloads and services.",
        ),
        Chunk(
            id=16,
            content="Blockchain: A decentralized ledger technology that records transactions across multiple computers.",
        ),
        Chunk(
            id=17,
            content="Serverless Computing: A cloud-computing model where the cloud provider runs the server, and dynamically manages the allocation of machine resources.",
        ),
        Chunk(
            id=18,
            content="Quantum Computing: A type of computing that uses quantum bits (qubits) to perform operations at incredibly high speeds.",
        ),
        Chunk(
            id=19,
            content="GraphQL: A query language for APIs that allows clients to request exactly the data they need.",
        ),
        Chunk(
            id=20,
            content="Edge Computing: A distributed computing paradigm that brings computation and data storage closer to the location where it is needed.",
        ),
    ]

    def __init__(self, project: Project):
        self.project = project

    def get_relevant_chunks(self, question: str) -> List[Chunk]:
        """
        In the real system this function contains the logic for doing semantic retrieval
        over the documents of a company. This means that the function returns the most closely
        related documents to the 'question' from the embeddings based index.


        For simplicity of this this excersice this was replaced with
        a dummy implementation. The function just returns 5 random documents evertime it is called.
        The documents themselves are just random technical descriptions as well.

        You do not have to make any changes here.
        """
        return random.sample(self.documents, 5)
