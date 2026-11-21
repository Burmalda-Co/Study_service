from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from .models import Assignment, Material, Test
from .serializers import AssignmentSerializer, MaterialSerializer, TestSerializer


class BaseStudyViewSet(viewsets.ModelViewSet):
    """Полный CRUD + поиск (?search=) и сортировка (?ordering=)."""

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ("title", "description")
    ordering_fields = ("id", "title", "created_at", "updated_at")


@extend_schema_view(
    list=extend_schema(summary="List materials"),
    create=extend_schema(summary="Create a material"),
    retrieve=extend_schema(summary="Get a material"),
    update=extend_schema(summary="Replace a material"),
    partial_update=extend_schema(summary="Update a material partially"),
    destroy=extend_schema(summary="Delete a material"),
)
@extend_schema(tags=["materials"])
class MaterialViewSet(BaseStudyViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    search_fields = ("title", "description", "content")


class MaterialFilterMixin:
    """Фильтр по связанному материалу: ?material=<id>."""

    def get_queryset(self):
        qs = super().get_queryset()
        material = self.request.query_params.get("material")
        if material and material.isdigit():
            qs = qs.filter(material_id=material)
        return qs


@extend_schema_view(
    list=extend_schema(summary="List assignments (filter: ?material=<id>)"),
    create=extend_schema(summary="Create an assignment"),
    retrieve=extend_schema(summary="Get an assignment"),
    update=extend_schema(summary="Replace an assignment"),
    partial_update=extend_schema(summary="Update an assignment partially"),
    destroy=extend_schema(summary="Delete an assignment"),
)
@extend_schema(tags=["assignments"])
class AssignmentViewSet(MaterialFilterMixin, BaseStudyViewSet):
    queryset = Assignment.objects.select_related("material")
    serializer_class = AssignmentSerializer
    ordering_fields = BaseStudyViewSet.ordering_fields + ("due_date", "max_score")


@extend_schema_view(
    list=extend_schema(summary="List tests (filter: ?material=<id>)"),
    create=extend_schema(summary="Create a test"),
    retrieve=extend_schema(summary="Get a test"),
    update=extend_schema(summary="Replace a test"),
    partial_update=extend_schema(summary="Update a test partially"),
    destroy=extend_schema(summary="Delete a test"),
)
@extend_schema(tags=["tests"])
class TestViewSet(MaterialFilterMixin, BaseStudyViewSet):
    queryset = Test.objects.select_related("material")
    serializer_class = TestSerializer
