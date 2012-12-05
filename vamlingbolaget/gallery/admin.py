from django.contrib import admin
from models import Image, Gallery, GalleryStatus, Photographer
from modeltranslation.admin import TranslationAdmin

class ImagesInLine(admin.TabularInline):
    model = Image     

class ImagesInline(ImagesInLine, TranslationAdmin):
    model = Image
    max_num=4
    extra=1

class ImageAdmin(TranslationAdmin):
    list_display = ('name', 'image', 'variation', 'is_featured','order','gallery', )
    list_editable = ('image', 'variation', 'is_featured','order',)
    list_filter = ('name', 'image', 'gallery', 'variation', 'is_featured',)
    ordering = ['name', 'gallery', 'variation']
    model = Image

class GalleryAdmin(TranslationAdmin):
    list_display = ('name', 'status', 'is_active', 'created_date','feature_image', )
    list_editable = ('status', 'is_active', 'feature_image',)
    list_filter = ('name', 'created_date',)
    ordering = ['name', 'created_date',]

    model = Gallery
    inlines = [
        ImagesInLine,
    ]

class GalleryStatusAdmin(TranslationAdmin):    
    list_display = ('name','display_on_gallery_page', 'display_on_index_page','order')
    list_display_links = ('display_on_gallery_page', 'display_on_index_page','order')
    list_editable = ('name',)
    model = GalleryStatus

class PhotographerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryStatus, GalleryStatusAdmin)
admin.site.register(Photographer, PhotographerAdmin)