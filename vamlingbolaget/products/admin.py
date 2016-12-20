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
    
class ArticleCostAdmin(admin.ModelAdmin):
    model = ArticleCost
    list_display = ('pk', 'article', 'fabric_m', 'cuttime', 'sawtime', 'addtime', 'attachment', 'get_final_cost', 'get_gross_cost', 'get_out_cost', 'get_current_price')
    list_display_links = ('pk', 'article',)
    list_editable = ('fabric_m', 'cuttime', 'sawtime', 'addtime', 'attachment',)
    list_per_page = 20
 
class FullVariationAdmin(admin.ModelAdmin):
    model = FullVariation
    list_display = ('active', 'variation', 'size', 'order', 'stock',)
    list_editable = ('active', 'stock',)
    list_display_links = ('variation',)
    list_filter = ('variation', 'size',)
    search_fields = ['variation']
    list_per_page = 20
    ordering = ['variation']


class ArticleAdmin(TranslationAdmin):
    model = Article
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'sku_number', 'name', 'description', 'price', 'type', 'quality', 'file', 'pk')
    list_display_links = ('active', )
    list_editable = ('file', 'name', 'description',)
    list_filter = ('active', 'type',)
    search_fields = ['sku_number', 'name']
    list_per_page = 20
    ordering = ['active', 'name']

class ReaArticleAdmin(admin.ModelAdmin):
    model = ReaArticle
    list_display = ('id', 'status','stockquantity', 'article', 'rea_price', 'pattern', 'color', 'quality', 'category', 'size', 'description', 'image')
    list_display_links = ('article', )
    list_editable = ('status', 'image')
    list_filter = ('status', 'article',)
    search_fields = ['sku_number', 'article',]
    list_per_page = 4
    ordering = ['status', 'id', ]


class ColorAdmin(TranslationAdmin):
    model = Color
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'name_da', 'order', 'quality',)
    list_display_links = ('name',)
    list_editable = ('active', 'order', 'quality', 'name_da',)
    list_filter = ('active',)
    ordering = ['order', 'name',]


class PatternAdmin(TranslationAdmin):
    model = Pattern
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('pk', 'active', 'name', 'name_da', 'order', 'quality', 'slug', )
    list_display_links = ('name',)
    list_editable = ('active', 'order', 'quality', 'name_da', )
    list_filter = ('active',)
    ordering = ['order', 'name',]

class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ('name', 'quality',)
    list_display_links = ('name',)
    list_editable = ('quality',)
    list_filter = ('quality',)

class PatternAndColorAdmin(admin.ModelAdmin):
    model = PatternAndColor
    list_display = ('name', 'color', 'pattern', 'quality',)
    list_display_links = ('name',)
    list_filter = ('quality',)

class QualityAdmin(TranslationAdmin):
    model = Quality
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'name_da', 'description', 'order',)
    list_display_links = ('name',)
    list_editable = ('active', 'order', 'name_da',)
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
admin.site.register(FullVariation, FullVariationAdmin)     
admin.site.register(Article, ArticleAdmin)
admin.site.register(ReaArticle, ReaArticleAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(PatternAndColor, PatternAndColorAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount)
admin.site.register(Bargainbox)
