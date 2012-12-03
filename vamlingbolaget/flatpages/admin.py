from django.contrib import admin
from django import forms
from gallery.models import Gallery
from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.forms import FlatpageForm as FlatpageFormOld
    

class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FlatPage

class GalleryInline(admin.TabularInline):
    model = Gallery

class FlatPageAdmin(TranslationAdmin,FlatPageAdminOld):
    #form = FlatpageForm
    inlines = [
        GalleryInline
    ]

    
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
                    
