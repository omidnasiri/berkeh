from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.drf import BerkehViewSet, CommentViewSet, LocationViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"berkehs", BerkehViewSet)
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r"locations", LocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
