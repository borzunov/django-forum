from itertools import zip_longest

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, TopicForm
from .models import Post, Section, Topic


def index(request):
    sections = Section.objects.order_by('position')

    return render(request, 'forum/index.html', {
        'section_rows': list(zip_longest(sections[::2], sections[1::2])),
    })


def show_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    topics = list(Topic.objects.filter(section_id=section_id))
    topics.sort(key=lambda topic: topic.last_message.created, reverse=True)

    return render(request, 'forum/section.html', {
        'section': section,
        'topics': topics,
    })


def show_topic(request, section_id, topic_id):
    topic = get_object_or_404(Topic, section_id=section_id, id=topic_id)
    posts = Post.objects.filter(topic_id=topic_id).order_by('created')

    return render(request, 'forum/topic.html', {
        'topic': topic,
        'posts': posts,
        'post_form': PostForm(),
    })


@login_required
def create_topic(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    return render(request, 'forum/create_topic.html', {
        'section': section,
        'form': TopicForm(),
    })


@login_required
def create_post(request, section_id, topic_id):
    if topic_id is not None:
        form = PostForm(request.POST)
        if not form.is_valid():
            return redirect('forum:show-topic', section_id=section_id, topic_id=topic_id)

        topic = get_object_or_404(Topic, section_id=section_id, id=topic_id)
    else:
        form = TopicForm(request.POST)
        if not form.is_valid():
            return redirect('forum:create-topic', section_id=section_id)

        section = get_object_or_404(Section, id=section_id)
        topic = Topic.objects.create(section=section, title=form.cleaned_data['topic_title'], author=request.user)

    Post.objects.create(topic=topic, content=form.cleaned_data['content'], author=request.user)
    return redirect('forum:show-topic', section_id=section_id, topic_id=topic.id)


@login_required
def delete_post(request, post_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Только администратор может удалять сообщения')

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('forum:show-topic', section_id=post.topic.section.id, topic_id=post.topic.id)
