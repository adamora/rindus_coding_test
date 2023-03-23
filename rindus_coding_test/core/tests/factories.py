from factory.django import DjangoModelFactory

from rindus_coding_test.core.models import Comment, Post


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
