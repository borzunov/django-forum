from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^profile/(?P<username>.+)/$', views.show, name='show'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<username>.+)/$', views.activate, name='activate'),

    url(r'^visitors/$', views.get_visitors, name='get-visitors'),
]
