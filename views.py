import os
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django_press_gallery.models import MediaSet as MediaSetModel, MediaGroup, MediaFiles
from sendfile import sendfile
from zipfile import ZipFile
import StringIO

class MediaSet(View):
    def get(self, request):
        return render(request, 'django_press_gallery/pressphotos.html', {
            'media_sets': MediaSetModel.objects.all()
        })


class Media(View):
    def get(self, request, id):
        media_set = get_object_or_404(MediaSetModel, pk=id)
        media = media_set.mediagroup_set.all()

        return render(request, 'django_press_gallery/media.html', {'media': media})

class DownloadFILE(View):
    def get(self, request, id):
        mediafile = get_object_or_404(MediaFiles, pk=id)
        return sendfile(
            request,
            mediafile.media_file.path,
            attachment=True,
            attachment_filename=mediafile.get_filename()
        )

class DownloadFileFormat(View):
    def get(self, request, media_type, mediaset_id=None):
        # media_files = MediaFiles.objects.filter(media_type=media_type)
        if mediaset_id:
            media_files = MediaFiles.objects.filter(mediagroup__mediaset_id=mediaset_id)
        else:
            media_files = MediaFiles.objects.all()

        # str_io = StringIO.StringIO()
        zip_file_name = '{media}/django_press_gallery/files.zip'.format(media=settings.MEDIA_ROOT)
        with ZipFile(zip_file_name, 'w') as file_zip:
            for media_file in media_files:
                fdir, fname = os.path.split(media_file.media_file.path)
                zip_path = os.path.join('files', fname)
                file_zip.write(media_file.media_file.path, zip_path)

        return sendfile(
            request,
            zip_file_name,
            attachment=True,
            # attachment_filename=zip_file_name.split('/')[-1]
        )
