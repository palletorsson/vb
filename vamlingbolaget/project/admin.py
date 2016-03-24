from django.contrib import admin
from models import Project, Media, File, Kanban

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('title', 'folder', 'status', 'prio', 'active',)
    list_display_links = ('title',)
    list_editable = ('status', 'prio', 'active', )
    list_filter = ('status', 'prio', 'active', )
    list_per_page = 20
    ordering = ['active']

class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ('title', 'link', 'type',)
    list_display_links = ('title',)
    list_per_page = 20


class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ('title', 'link', 'status',)
    list_display_links = ('title',)
    list_per_page = 20


class KanbanAdmin(admin.ModelAdmin):
    model = File
    list_display = ('title', 'link',)
    list_display_links = ('title',)
    list_per_page = 20

admin.site.register(Project, ProjectAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Kanban, KanbanAdmin)
