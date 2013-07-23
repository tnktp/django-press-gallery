from django.db import models
from stdimage import StdImageField
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ['^stdimage\.fields\.StdImageField'])

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MediaSet(BaseModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.title

    def get_thumbnail_url(self):
        media_items = self.mediagroup_set.all()
        if media_items:
            first_media_item = media_items[0]
            media_files = first_media_item.mediafiles_set.all()
            if media_files:
                first_media_file = media_files[0]
                return first_media_file.media_file.thumbnail.url()
        return ''


class MediaGroup(BaseModel):
    mediaset = models.ForeignKey(MediaSet)
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Media revision"


class MediaFiles(BaseModel):
    media = models.ForeignKey(MediaGroup)
    # mediaset = models.ForeignKey(MediaSet)
    # parent_media = models.ForeignKey('self', null=True, blank=True)
    media_file = StdImageField(upload_to='django_press_gallery_uploads', thumbnail_size=(215, 215))
    media_type = models.CharField(max_length=50, null=True, blank=True, editable=False)
    description = models.TextField(null=True, blank=True)
    # TODO: Change files to file field so that It can work for other media types and not just images

    def __unicode__(self):
        return r'{file_name} | {file_description}'.format(
            file_name=self.get_filename(), file_description=self.description
        )

    def get_filename(self):
        return self.media_file.url.split('/')[-1]
