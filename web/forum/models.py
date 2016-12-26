from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import truncatechars


class Section(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    position = models.IntegerField(default=0)

    @property
    def recent_topics(self):
        topics = list(Topic.objects.filter(section_id=self.id))
        topics.sort(key=lambda topic: topic.last_message.created, reverse=True)
        return topics[:2]

    def __str__(self):
        return '{} ({})'.format(self.title, self.position)


class Topic(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    title = models.CharField(max_length=256)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def last_message(self):
        return Post.objects.filter(topic_id=self.id).order_by('-created').first()

    def __str__(self):
        return '{} / {} ({})'.format(self.section.title, self.title, self.author.username)


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(blank=True, null=True)

    @property
    def author_profile(self):
        Profile = apps.get_model('profiles', 'Profile')
        return Profile.objects.get(id=self.author.id)

    def __str__(self):
        return '{} / {} / {} ({})'.format(
            self.topic.section.title, self.topic.title, truncatechars(self.content, 30), self.author.username)
