from django.contrib import admin
from models import Page

from modeltranslation.admin import TranslationAdmin

class PageAdmin(TranslationAdmin):
    model = Page
    list_display = ('title', 'url', 'active',)
    list_filter = ('title',)
    list_per_page = 20
    ordering = ['title',]

admin.site.register(Page, PageAdmin)