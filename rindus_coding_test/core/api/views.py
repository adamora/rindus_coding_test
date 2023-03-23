from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rindus_coding_test.core.api.serializers import CommentSerializer, PostSerializer
from rindus_coding_test.core.models import Comment, Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
