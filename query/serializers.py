from typing import Optional

from rest_framework import serializers

from query.models import Thread


class ChatInputSerializer(serializers.Serializer):
    """
    Serializer for the input to the chat view
    """

    question = serializers.CharField(help_text="The question to generate an answer for")
    thread_id = serializers.UUIDField(
        required=False,
        help_text="Specify a thread if you want to continue a conversation",
    )


class ChatOutputSerializer(serializers.Serializer):
    """
    Serializer for the output of the chat view
    """

    question = serializers.CharField()
    answer = serializers.CharField()
    question_answer_id = serializers.UUIDField(
        help_text="The id of the generated question answer",
    )
    thread_id = serializers.UUIDField(
        help_text="The id of the generated thread",
    )


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Thread' model
    """

    first_question = serializers.SerializerMethodField(allow_null=True)
    total_questions = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "project",
            "created_at",
            "first_question",
            "total_questions",
        ]

    def get_first_question(self, obj) -> Optional[str]:
        """
        Returns the first question of the thread if there is one
        """
        first_question_answer = obj.question_answers.order_by("created_at").first()
        return first_question_answer.question if first_question_answer else None

    def get_total_questions(self, obj) -> int:
        """
        Returns the total number of questions associated with the thread
        """
        return obj.question_answers.count()
