from django.contrib import admin
from models import *
from gallery.models import Image, Gallery

class VariationImageInline(admin.StackedInline):
  model = Image
  max_num=4
  extra=1

class VariationAdmin(admin.ModelAdmin):
    model = Variation
    inlines = [VariationImageInline,]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'article', 'pattern','color',)
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('created_at', 'updated_at', 'active', 'article',)
    search_fields = ['name']
    list_per_page = 20
    ordering = ['active','name']

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'sku_number', 'name', 'price', 'type', 'quality', 'file')
    list_display_links = ('name', )
    list_editable = ('active','file', )
    list_filter = ('active', 'type',)
    search_fields = ['sku_number', 'name']
    list_per_page = 20
    ordering = ['active', 'name']

class ColorAdmin(admin.ModelAdmin):
    model = Color
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'order',)
    list_display_links = ('name',)
    list_editable = ('active', 'order',)
    list_filter = ('active',)
    ordering = ['order', 'name',]


class PatternAdmin(admin.ModelAdmin):
    model = Pattern
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'order')
    list_display_links = ('name',)
    list_editable = ('active', 'order',)
    list_filter = ('active',)
    ordering = ['order', 'name',]

class SizeAdmin(admin.ModelAdmin):
    model = Size

class QualityAdmin(admin.ModelAdmin):
    model = Quality
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'description', 'order',)
    list_display_links = ('name',)
    list_editable = ('active', 'order',)
    list_filter = ('active', )
    ordering = ['order']
    
class TypeAdmin(admin.ModelAdmin):
    model = Type
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'order',)
    list_display_links = ('name',)
    list_editable = ('active', 'order',)
    list_filter = ('active', )
    ordering = ['order']

admin.site.register(Variation, VariationAdmin)    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(Type, TypeAdmin)

