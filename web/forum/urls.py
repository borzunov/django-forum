from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<section_id>\d+)/$', views.show_section, name='show-section'),
    url(r'^(?P<section_id>\d+)/(?P<topic_id>\d+)/$', views.show_topic, name='show-topic'),
    url(r'^(?P<section_id>\d+)/create/$', views.create_topic, name='create-topic'),
    url(r'^(?P<section_id>\d+)(?:/(?P<topic_id>\d+))?/post/$', views.create_post, name='create-post'),
]
