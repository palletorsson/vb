from django.core.urlresolvers import reverse
from django.contrib import admin
from django.conf import settings
from models import Blog, Post, New
from django import forms
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from gallery.models import Gallery
from modeltranslation.admin import TranslationAdmin

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'description', 'user')
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('modified', 'created', 'active')


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {
            'fields': ('title', 'blog'),
	}),
	('Publication', {
            'fields': ('active', 'publish_at'),
	    'description': "visable"
	}),
	('Content', {
            'fields': ('body', 'tags'),
	}),
	('Optional', {
            'fields': ('slug',),
	    'classes': ('collapse',),
	})
    )
    search_fields = ['title','excerpt', 'body']
    list_display = ('active', 'title', 'publish_at')
    list_display_links = ('title',)
    list_editable = ('active', 'publish_at')
    list_filter = ('modified', 'created', 'active')


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
    (None, {
        'fields': ('title',),
        }),
    ('Publication', {
        'fields': ('active', 'publish_at'),
        'description': "visable"
    }),
    ('Content', {
        'fields': ('body',),
        }),
    ('Optional', {
        'fields': ('slug',),
        'classes': ('collapse',),
        })
    )
search_fields = ['title', 'body']
list_display = ('active', 'title', 'publish_at')
list_display_links = ('title',)
list_editable = ('active', 'publish_at')
list_filter = ('modified', 'created', 'active')


admin.site.register(Post, PostAdmin)

admin.site.register(New, NewsAdmin)

admin.site.register(Blog, BlogAdmin)
