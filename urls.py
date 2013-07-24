from django.conf.urls import patterns, url
from django_press_gallery.views import MediaSet, Media, DownloadFILE, DownloadFileFormat, Login
 
urlpatterns = patterns('',
    url(r'^/$', MediaSet.as_view(), name='home'),
    url(r'^/(?P<id>\d+)/([\w-]+)$', Media.as_view(), name='media'),
    url(r'^/download/(?P<id>\d+)$', DownloadFILE.as_view(), name='download'),
    url(r'^/download_files/(?P<mediaset_id>\d+)/(?P<version>[\w-]+)$', DownloadFileFormat.as_view(), name='download_files'),
    url(r'/login', Login.as_view(), name='login')
)