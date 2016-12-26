from django.apps import apps
from django.contrib.auth.models import User
from django.db import models


class Profile(User):
    class Meta:
        proxy = True

    @property
    def post_count(self):
        Post = apps.get_model('forum', 'Post')
        return Post.objects.filter(author=self).count()

    @property
    def new_topic_count(self):
        Topic = apps.get_model('forum', 'Topic')
        return Topic.objects.filter(author=self).count()


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now_add=True)
