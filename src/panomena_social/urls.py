from django.conf.urls.defaults import *


urlpatterns = patterns('panomena_social.views',
    url(r'^(?P<content_type>[\w\-\+\.]+)/(?P<pk>\d+)/like/$', 'like', {}, 'social_like'),
    url(r'^(?P<content_type>[\w\-\+\.]+)/(?P<pk>\d+)/like/$', 'unlike', {}, 'social_unlike'),
)
