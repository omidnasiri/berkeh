from rest_framework import serializers
from .models import Berkeh, Location, BerkehPhoto, Comment


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class BerkehPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BerkehPhoto
        fields = "__all__"


class BerkehSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    photos = BerkehPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Berkeh
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
