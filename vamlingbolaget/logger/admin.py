from django.contrib import admin
from models import LogItem

class LogItemAdmin(admin.ModelAdmin):
    model = LogItem
    list_display = ('date_added', 'title', 'log_level', 'ip', 'session_key', )
    list_display_links = ('title',)
    list_editable = ('log_level',)
    list_per_page = 20
    ordering = ['-id',]

admin.site.register(LogItem, LogItemAdmin)
