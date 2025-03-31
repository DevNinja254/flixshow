from rest_framework import serializers
from .models import *

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Like
        fields = "__all__"
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = "__all__"
class VideoUploadSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = VideoUpload
        fields = "__all__"
class CartegoriesSerializer(serializers.ModelSerializer):
    video_details = VideoUploadSerializer(many=True, read_only=True)
    class Meta:
        model = Cartegories
        fields = "__all__"
class videosSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = videos
        fields = "__all__"