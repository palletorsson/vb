from django.contrib import admin
from models import *
from gallery.models import Image, Gallery
from modeltranslation.admin import TranslationAdmin

class VariationImageInline(admin.StackedInline):
  model = Image
  max_num=4
  extra=1

class VariationAdmin(admin.ModelAdmin):
    model = Variation
    inlines = [VariationImageInline,]
    list_display = ('active', 'article', 'pattern', 'color', 'order',)
    list_display_links = ('article',)
    list_editable = ('active', 'order', 'pattern', 'color',)
    list_filter = ('active', 'article', 'pattern', 'color',)
    search_fields = ['article']
    list_per_page = 20
    ordering = ['active','article']


class ArticleAdmin(TranslationAdmin):
    model = Article
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'sku_number', 'name', 'price', 'type', 'quality', 'file')
    list_display_links = ('name', )
    list_editable = ('active','file', )
    list_filter = ('active', 'type',)
    search_fields = ['sku_number', 'name']
    list_per_page = 20
    ordering = ['active', 'name']

class ColorAdmin(TranslationAdmin):
    model = Color
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'order', 'quality',)
    list_display_links = ('name',)
    list_editable = ('active', 'order', 'quality',)
    list_filter = ('active',)
    ordering = ['order', 'name',]


class PatternAdmin(TranslationAdmin):
    model = Pattern
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'order', 'quality',)
    list_display_links = ('name',)
    list_editable = ('active', 'order', 'quality',)
    list_filter = ('active',)
    ordering = ['order', 'name',]

class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ('name', 'quality',)
    list_display_links = ('name',)
    list_editable = ('quality',)
    list_filter = ('quality',)

class QualityAdmin(TranslationAdmin):
    model = Quality
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'description', 'order',)
    list_display_links = ('name',)
    list_editable = ('active', 'order',)
    list_filter = ('active', )
    ordering = ['order']
    
class TypeAdmin(TranslationAdmin):
    model = Type
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'order',)
    list_display_links = ('name',)
    list_editable = ('active', 'order',)
    list_filter = ('active', )
    ordering = ['order']

class CategoryAdmin(TranslationAdmin):
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
admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount)
admin.site.register(Bargainbox)