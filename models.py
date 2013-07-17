from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MediaSet(BaseModel):
    title = models.CharField(max_length=250)
    thumbnail = models.ImageField(
        upload_to='django_press_gallery/mediaset_thumbnail/%Y/%m/%d'
    )


class Media(BaseModel):
    mediaset = models.ForeignKey(MediaSet)
    thumbnail = models.ImageField(
        upload_to='django_press_gallery/media_thumbnail/%Y/%m/%d'
    )


class MediaFiles(BaseModel):
    media = models.ForeignKey(Media)
    media_file = models.ImageField(upload_to='mediafiles_files')
    media_type = models.CharField(max_length=50, null=True, blank=True, editable=False)
    description = models.TextField(null=True, blank=True, editable=False)
    # TODO: Change files to file field so that It can work for other media types and not just images


