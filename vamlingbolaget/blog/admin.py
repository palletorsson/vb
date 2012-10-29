from django.core.urlresolvers import reverse
from django.contrib import admin
from django.conf import settings
from models import Blog, Post

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from tinymce.widgets import TinyMCE


class EventAdmin(admin.ModelAdmin):
    class Media:
        js = (settings.TINYMCE_JS_URL,
              settings.FILEBROWSER_JS_URL,)

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

    class Media:
        js = (settings.TINYMCE_JS_URL,
              settings.FILEBROWSER_JS_URL,)

class TinyMCEPostAdmin(PostAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'body':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(TinyMCEPostAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Post, TinyMCEPostAdmin)

admin.site.register(Blog, BlogAdmin)


class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    class Meta:
        model = FlatPage


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)
