from django.db import models


class Post(models.Model):
    user_id = models.IntegerField(default="99999942")
    title = models.CharField(max_length=255)
    body = models.TextField()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
