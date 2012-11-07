from django.contrib import admin
from models import Image, Gallery


class ImageAdmin(admin.ModelAdmin):
    model = Image

class GalleryAdmin(admin.ModelAdmin):
    model = Gallery


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
