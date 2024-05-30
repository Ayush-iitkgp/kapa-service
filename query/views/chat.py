import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from org.models import Project
from org.permissions import HasProjectAPIKey
from query.models import Thread
from query.serializers import ChatInputSerializer, ChatOutputSerializer
from query.src.rag_agent import RAGAgent
from query.tasks import classify_thread

logger = logging.getLogger(__name__)


class ChatView(APIView):
    permission_classes = [HasProjectAPIKey]

    def post(self, request, project_id, format=None):
        """
        This endpoint serves the chat logic
        """
        project = get_object_or_404(Project, id=project_id)

        # Valdiate the input data
        serializer = ChatInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        question = validated_data["question"]
        thread_id = validated_data.get("thread_id", None)

        # Generate an answer
        rag_agent = RAGAgent(project=project)

        if thread_id:
            # Follow up question
            thread = get_object_or_404(Thread, id=thread_id)
            result = rag_agent.generate_follow_up_answer(
                question=question, thread=thread
            )
        else:
            # First queston
            result = rag_agent.generate_answer(question)
            classify_thread.apply_async(
                kwargs={"question_answer_id": str(result["question_answer_id"])}
            )

        # Serialize the response data
        response_serializer = ChatOutputSerializer(data=result)
        if not response_serializer.is_valid():
            logger.error(
                f"ChatOutputSerializer validation failed: {response_serializer.errors}"
            )
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(response_serializer.data, status=status.HTTP_200_OK)
