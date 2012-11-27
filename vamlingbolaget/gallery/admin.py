from django.contrib import admin
from models import Image, Gallery

class ImagesInLine(admin.TabularInline):
    model = Image
    

class ImageAdmin(admin.ModelAdmin):
    model = Image

class GalleryAdmin(admin.ModelAdmin):
    model = Gallery
    inlines = [
        ImagesInLine
    ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
