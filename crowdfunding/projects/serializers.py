from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Project, Pledge, Comment

User = get_user_model()

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.SlugRelatedField(
        slug_field= 'username', 
        queryset= get_user_model().objects.all()
    )
    project_id = serializers.IntegerField()
    supporter = serializers.ReadOnlyField(source='supporter.id')

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.id')
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    
    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only="true",
    )

    class Meta:
        model = Comment
        exclude = ['visible']


class ProjectCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only="true",
    )
    class Meta:
        model = Comment
        exclude = ["visible", "project"]


    
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField()

    def create(self, validated_data):
        return Category.objects.create(**validated_data)