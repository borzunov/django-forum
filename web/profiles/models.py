from django.apps import apps
from django.contrib.auth.models import User


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
