from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import authenticate
from .models import User, Post, Like, Tag
from .serializers import UserSignupSerializer, PostSerializer, PostListSerializer
from django.utils import timezone

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({"message": "User logged in successfully."})
    
class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, created_at=timezone.now())

class PublishPostView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk, author=request.user)
            post.is_published = not post.is_published
            post.save()
            return Response({'status': 'published' if post.is_published else 'unpublished'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

class UnpublishPostView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk, author=request.user)
            if post.is_published:
                post.is_published = False
                post.save()
                return Response({'status': 'unpublished'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Post is already unpublished'}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        
class ListPostsView(generics.ListAPIView):
    serializer_class = PostListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

class LikePostView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                like.delete()
                return Response({'status': 'unliked'})
            return Response({'status': 'liked'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

