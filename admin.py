from django.contrib import admin
from django_press_gallery import models


admin.site.register(models.MediaSet)
# admin.site.register(models.MediaFiles)

class MediaFilesInline(admin.StackedInline):
    model = models.MediaFiles
    extra  = 0

class MediaGroupAdmin(admin.ModelAdmin):
    inlines = [MediaFilesInline]

admin.site.register(models.MediaGroup, MediaGroupAdmin)

'''
class ProductImageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ImageField: {'widget': FileInput(attrs={'multiple': 'multiple'})},
    }

    def save_model(self, request, obj, form, change):
        for afile in request.FILES.getlist('image'):
            models.ProductImage(image=afile).save()

admin.site.register(models.ProductImage, ProductImageAdmin)


class ProductAvailableColorInline(admin.StackedInline):
    model = models.ProductAvailableColor
    extra  = 0

class ProductColorsIncludedInline(admin.StackedInline):
    model = models.ProductColorsIncluded
    extra  = 0

class ProductNumberInline(admin.StackedInline):
    model = models.ProductNumber
    extra  = 0

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProductAvailableColorInline,
        ProductColorsIncludedInline,
        ProductNumberInline
    ]

admin.site.register(models.Product, ProductAdmin)
'''