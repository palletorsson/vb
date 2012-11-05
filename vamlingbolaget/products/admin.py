from django.contrib import admin
from models import *

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
    list_display = ('active', 'sku_number', 'name', 'price', 'type', 'quality',)
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('active', 'type',)
    search_fields = ['sku_number', 'name']
    list_per_page = 20
    ordering = ['active', 'name']
    
class ColorAdmin(admin.ModelAdmin):
    model = Color
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active',)
    
class PatternAdmin(admin.ModelAdmin):
    model = Pattern
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active',)
    ordering = ['order']

class SizeAdmin(admin.ModelAdmin):
    model = Size


class QualityAdmin(admin.ModelAdmin):
    model = Quality
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'description')
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', )
    ordering = ['order']
    
class TypeAdmin(admin.ModelAdmin):
    model = Type
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'slug',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', )
    ordering = ['order']

class ImageVariationAdmin(admin.ModelAdmin):
    model = Image

    

admin.site.register(Variation, VariationAdmin)    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Image, ImageVariationAdmin)

admin.site.register(Gallery)

