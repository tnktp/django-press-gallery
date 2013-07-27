import os, shutil
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.functional import Promise
from stdimage import StdImageField

class LazyEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyEncoder, self).default(o)

class JSONResponse(HttpResponse):
    def __init__(self, status, data={}):
        HttpResponse.__init__(
            self, content=simplejson.dumps(data, cls=LazyEncoder),
            mimetype="application/json",
            status=status,
        )


class DPGImageField(StdImageField):
    def _resize_image(self, filename, size):
        """Resizes the image to specified width, height and force option

        Arguments::

        filename -- full path of image to resize
        size -- dictionary with
            - width: int
            - height: int
            - force: bool
                if True, image will be cropped to fit the exact size,
                if False, it will have the bigger size that fits the specified
                size, but without cropping, so it could be smaller on width
                or height

        """

        WIDTH, HEIGHT = 0, 1
        try:
            import Image, ImageOps
        except ImportError:
            from PIL import Image, ImageOps
        img = Image.open(filename)
        if (img.size[WIDTH] > size['width'] or
            img.size[HEIGHT] > size['height']):

            #If the image is big resize it with the cheapest resize algorithm
            # factor = 1
            # while (img.size[0]/factor > 2*size['width'] and
            #        img.size[1]*2/factor > 2*size['height']):
            #     factor *=2
            # if factor > 1:
            #     img.thumbnail((int(img.size[0]/factor),
            #                    int(img.size[1]/factor)), Image.NEAREST)

            if size['force']:
                img = ImageOps.fit(img, (size['width'], size['height']),
                                   Image.ANTIALIAS)
            else:
                img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _rename_resize_image(self, instance=None, **kwargs):
        """Renames the image, and calls methods to resize and create the
        thumbnail.

        """
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            
            if self.size:
                self._resize_image(filename, self.size)
                
            if self.thumbnail_size:
                thumbnail_filename = self._get_thumbnail_filename(filename)
                shutil.copyfile(filename, thumbnail_filename)
                self._resize_image(thumbnail_filename, self.thumbnail_size)