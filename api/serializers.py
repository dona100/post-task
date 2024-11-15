from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Post, Tag, Like

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )
    tags_display = serializers.SerializerMethodField()  # For displaying tag names in the response

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'tags_display', 'created_at', 'is_published']
        read_only_fields = ['tags_display']

    def get_tags_display(self, obj):
        # Returns a list of tag names associated with the post
        return [tag.name for tag in obj.tags.all()]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)
        return post




class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y')
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_at', 'is_published', 'likes_count']
