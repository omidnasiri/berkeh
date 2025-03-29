from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BerkehViewSet, CommentViewSet, LocationViewSet

router = DefaultRouter()
router.register(r"berkehs", BerkehViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"locations", LocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
