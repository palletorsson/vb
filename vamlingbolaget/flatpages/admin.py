from django.contrib.flatpages import admin
from django.contrib import admin
from models import Flatpage
from gallery.models import Gallery

class GalleryInline(admin.TabularInline):
    model = Gallery
    
    
class FlatPagesAdminXtra(FlatPageAdmin):
    model = Flatpage
    inlines = [
        GalleryInline
    ]
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'gallery')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )



admin.site.unregister(FlatPage, FlatPageAdmin)
admin.site.register(Flatpage, FlatPagesAdminXtra)
