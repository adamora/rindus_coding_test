from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rindus_coding_test.fake_rest_api.api.serializers import PostSerializer, CommentSerializer
from rindus_coding_test.fake_rest_api.models import Post, Comment


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
