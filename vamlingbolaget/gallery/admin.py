from django.contrib import admin
from models import Image, Gallery

class ImagesInLine(admin.TabularInline):
    model = Image
    

class ImagesInline(admin.StackedInline):
    model = Image
    max_num=4
    extra=1

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'variation', 'is_featured', )
    list_editable = ('image', 'variation', 'is_featured',)
    #inlines = [ImagesInline,]
    list_filter = ('name', 'image', 'gallery', 'variation', 'is_featured',)
    ordering = ['name', 'gallery', 'variation']

    model = Image

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_active', 'created_date','feature_image',  )
    list_editable = ('status', 'is_active', 'feature_image',)
    #inlines = [ImagesInline,]
    list_filter = ('name', 'created_date',)
    ordering = ['name', 'created_date',]

    model = Gallery
    inlines = [
        ImagesInLine
    ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
