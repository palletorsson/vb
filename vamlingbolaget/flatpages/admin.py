from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib import admin
from models import Flatpage
from gallery.models import Gallery
from modeltranslation.admin import TranslationAdmin

class GalleryInline(admin.TabularInline):
    model = Gallery
    
    
class FlatPagesAdminXtra(TranslationAdmin,FlatPageAdmin):
    model = Flatpage
    inlines = [
        GalleryInline
    ]
    


admin.site.unregister(FlatPage)
admin.site.register(Flatpage, FlatPagesAdminXtra)
