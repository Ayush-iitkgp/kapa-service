from django.contrib import admin
from django.db import models
from django.utils.text import Truncator

from .models import QuestionAnswer, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "created_at")


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "created_at",
        "thread_id",
        "truncated_question",
        "truncated_answer",
    )

    ordering = ("-created_at",)

    def project(self, obj):
        return obj.thread.project

    def thread_id(self, obj):
        return obj.thread.id

    def truncated_question(self, obj):
        return Truncator(obj.question).chars(50)

    truncated_question.short_description = "Question"

    def truncated_answer(self, obj):
        return Truncator(obj.answer).chars(50)

    truncated_answer.short_description = "Answer"

    search_fields = ["question", "answer"]

    list_filter = ("thread__project",)  # Filter by project
