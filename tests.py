from StringIO import StringIO
from zipfile import ZipFile
import mock
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.files.temp import NamedTemporaryFile
from django_press_gallery.views import DownloadFILE, DownloadFileFormat


class SimpleTest(TestCase):
    def setUp(self):
        self.user = mock.Mock()
        self.user.is_authenticated.return_value = True
        self.factory = RequestFactory()
        self.test_image1 = new_tmp_file = NamedTemporaryFile(prefix='test_image1', suffix='.png')
        self.test_image2 = new_tmp_file = NamedTemporaryFile(prefix='test_image2', suffix='.png')

    def test_download_file(self):
        def mock_get_object_or_404(*args, **kwargs):
            mediafile = mock.Mock()
            media_file = mock.Mock()
            
            media_file.path = self.test_image1.name
            mediafile.media_file = media_file
            mediafile.get_filename.return_value = 'test_image1.png'
            return mediafile 

        with mock.patch('django_press_gallery.views.get_object_or_404', mock_get_object_or_404):
            req = self.factory.get('/pressphotos/download/1')
            req.user = self.user
            res = DownloadFILE.as_view()(req, 1)
            self.assertEqual(res.status_code, 200)
            self.assertEquals(res.get('Content-Disposition'), 'attachment; filename="test_image1.png"')

    def test_download_file_format(self):
        def mock_get_object_or_404(*args, **kwargs):
            media_set = mock.Mock()
            media_set.slug = 'test-media-set'
            media_set.pk = 5
            return media_set 

        with mock.patch('django_press_gallery.views.get_object_or_404', mock_get_object_or_404):
            file_names = ['test_image1.png', 'test_image2.png']
            files = [self.test_image1, self.test_image2]
            mediafile_filter_list = []
            for i in range(2):
                mediafile = mock.Mock()
                media_file = mock.Mock()
                
                media_file.path = files[i].name
                mediafile.media_file = media_file
                mediafile.get_filename.return_value = file_names[i]
                mediafile_filter_list.append(mediafile)

            mediafiles = mock.Mock()
            objects = mock.Mock()
            objects.filter.return_value = mediafile_filter_list
            mediafiles.objects = objects

            with mock.patch('django_press_gallery.views.MediaFiles', mediafiles):
                req = self.factory.get('/pressphotos/download_files/4/rgb')
                req.user = self.user
                res = DownloadFileFormat.as_view()(req, 'rgb', 4)
                self.assertEqual(res.status_code, 200)
                self.assertEquals(res.get('Content-Disposition'), 'attachment; filename="test-media-set-5-rgb-files.zip"')

