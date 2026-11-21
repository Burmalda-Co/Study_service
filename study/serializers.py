from rest_framework import serializers

from .models import Assignment, Material, Test


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ("id", "title", "description", "content", "url", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            "id", "title", "description", "material", "due_date", "max_score",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id", "title", "description", "material", "time_limit_minutes",
            "passing_score", "is_published", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
