from django.conf.urls import patterns, url
from am_distribution.views import MediaSet, Media, DownloadFILE, DownloadFileFormat, Login
 
urlpatterns = patterns('',
    url(r'^/$', MediaSet.as_view(), name='am_distribution_home'),
    url(r'^/(?P<id>\d+)/([\w-]+)$', Media.as_view(), name='am_distribution_media'),
    url(r'^/download/(?P<id>\d+)$', DownloadFILE.as_view(), name='am_distribution_download'),
    url(r'^/download_files/(?P<mediaset_id>\d+)/(?P<version>[\w-]+)$', DownloadFileFormat.as_view(), name='am_distribution_download_files'),
    url(r'/login', Login.as_view(), name='login')
)