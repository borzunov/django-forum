from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^profile/(?P<username>.+)/$', views.show, name='show'),

    url(r'^signup/$', views.signup, name='signup'),
]
