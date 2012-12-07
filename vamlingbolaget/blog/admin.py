from django.contrib import admin
from models import Blog, Post, New
from django.conf import settings

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'description', 'user')
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('modified', 'created', 'active', )
    class Media:
        js = (settings.STATIC_URL+'tiny_mce/tiny_mce_src.js',
              settings.STATIC_URL+"filebrowser/js/TinyMCEAdmin.js",)

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
    list_display = ('active', 'title', 'publish_at', 'blog')
    list_display_links = ('title',)
    list_editable = ('active', 'publish_at')
    list_filter = ('modified', 'created', 'active', 'blog')


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
