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
class LimitedLatestRelatedObjectsField(serializers.ListField):
    def to_representation(self, queryset):
        # Limit the number of related objects to 3
        limited_queryset = queryset.order_by("-date_uploaded")[:13]
        serializer = VideoUploadSerializer(limited_queryset,many=True, read_only=True)
        return serializer.data
class CartegoriesSerializer(serializers.ModelSerializer):
    video_details = LimitedLatestRelatedObjectsField()
    total_related_count = serializers.SerializerMethodField()
    class Meta:
        model = Cartegories
        fields = "__all__"
    def get_total_related_count(self, instance):
        return instance.video_details.count()
class CartegoriesTotalSerializer(serializers.ModelSerializer):
    total_related_count = serializers.SerializerMethodField()
    class Meta:
        model = Cartegories
        fields = "__all__"
    def get_total_related_count(self, instance):
        return instance.video_details.count()
class videosSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = videos
        fields = "__all__"
