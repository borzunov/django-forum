from itertools import zip_longest

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post, Section, Topic


def index(request):
    sections = Section.objects.order_by('position')

    return render(request, 'forum/index.html', {
        'section_rows': list(zip_longest(sections[::2], sections[1::2])),
    })


def show_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    topics = Topic.objects.filter(section_id=section_id)

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
    })


@login_required
def create_topic(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    return render(request, 'forum/create_topic.html', {
        'section': section,
    })


@login_required
def create_post(request, section_id, topic_id):
    if topic_id is not None:
        redirect_back = redirect('forum:show-topic', section_id=section_id, topic_id=topic_id)
    else:
        redirect_back = redirect('forum:create-topic', section_id=section_id)

    if topic_id is not None:
        topic = get_object_or_404(Topic, section_id=section_id, id=topic_id)
    else:
        section = get_object_or_404(Section, id=section_id)

        title = request.POST.get('topic-title')
        if not title:
            messages.error(request, 'Название темы не может быть пустым')
            return redirect_back

        topic = Topic.objects.create(section=section, title=title, author=request.user)

    content = request.POST.get('content')
    if not content:
        messages.error(request, 'Сообщение не может быть пустым')
        return redirect_back

    Post.objects.create(topic=topic, content=content, author=request.user)
    return redirect('forum:show-topic', section_id=section_id, topic_id=topic.id)
