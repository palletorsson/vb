from django.contrib import admin

from blog.models import Blog, Post


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
            'fields': ('excerpt', 'body', 'tags'),
	}),
	('Optional', {
            'fields': ('slug',),
	    'classes': ('collapse',),
	})
    )
    search_fields = ['title','excerpt', 'body']
    list_display = ('active', 'title', 'excerpt', 'publish_at')
    list_display_links = ('title',)
    list_editable = ('active', 'publish_at')
    list_filter = ('modified', 'created', 'active')
        

	
admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)