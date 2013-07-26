import os
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django_press_gallery.models import MediaSet as MediaSetModel, MediaGroup, MediaFiles
from . import JSONResponse
from sendfile import sendfile
from zipfile import ZipFile
import StringIO

class LoginRequired(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated(), login_url='/pressphotos/login'))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)

class Login(View):
    def get(self, request):
        return render(request, 'django_press_gallery/login.html')

    def post(self, request):
        username = settings.LANDING_PAGE_LOGIN_USERNAME
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JSONResponse(201)
        return JSONResponse(400)
        

class MediaSet(LoginRequired):
    def get(self, request):
        return render(request, 'django_press_gallery/pressphotos.html', {
            'media_sets': MediaSetModel.objects.all()
        })


class Media(LoginRequired):
    def get(self, request, id):
        media_set = get_object_or_404(MediaSetModel, pk=id)
        media = media_set.mediagroup_set.all().order_by('title')

        # Get unique list of media discriptions
        versions = (MediaFiles.objects
                              .filter(media__mediaset_id=id)
                              .values_list('slug', flat=True)
                              .distinct())

        return render(request, 'django_press_gallery/media.html', {
            'media': media,
            'media_set': media_set,
            'versions': versions
        })

class DownloadFILE(LoginRequired):
    def get(self, request, id):
        mediafile = get_object_or_404(MediaFiles, pk=id)
        return sendfile(
            request,
            mediafile.media_file.path,
            attachment=True,
            attachment_filename=mediafile.get_filename()
        )

class DownloadFileFormat(LoginRequired):
    def get(self, request, version, mediaset_id):
        media_set = get_object_or_404(MediaSetModel, pk=mediaset_id)
        media_files = MediaFiles.objects.filter(
            description=version,
            media__mediaset_id=media_set.pk
        )

        file_name = '{media_set_name}-{mediaset_id}-{version}-files'.format(
            media_set_name=media_set.slug,
            mediaset_id=media_set.pk,
            version=version
        )
        zip_file_name_and_path = '{media}/django_press_gallery_uploads/{file_name}.zip'.format(
            media=settings.MEDIA_ROOT,
            file_name=file_name
        )

        if not os.path.exists(zip_file_name_and_path):
            with ZipFile(zip_file_name_and_path, 'w') as file_zip:
                for media_file in media_files:
                    fdir, fname = os.path.split(media_file.media_file.path)
                    zip_path = os.path.join(file_name, fname)
                    file_zip.write(media_file.media_file.path, zip_path)

        return sendfile(
            request,
            zip_file_name_and_path,
            attachment=True
        )
