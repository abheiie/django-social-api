from rest_framework.serializers import ModelSerializer, SerializerMethodField, RelatedField
from masterapp.models import Couser, Contact, Report, Post, Comment
from rest_framework import serializers


class CouserSerializer(ModelSerializer):
    class Meta:
        model = Couser
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'