from rest_framework.routers import DefaultRouter

from .views import AssignmentViewSet, MaterialViewSet, TestViewSet

router = DefaultRouter()
router.register("materials", MaterialViewSet, basename="material")
router.register("assignments", AssignmentViewSet, basename="assignment")
router.register("tests", TestViewSet, basename="test")

urlpatterns = router.urls
