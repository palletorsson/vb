from django.contrib import admin
from models import *

class VariationImageInline(admin.StackedInline):
  model = ImageVariation
  max_num=4
  extra=1
  
class CartAdmin(admin.ModelAdmin):
    model = CartItem


class VariationAdmin(admin.ModelAdmin):
    model = Variation
    inlines = [VariationImageInline,]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'name', 'article', 'combo', 'image')
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('created_at', 'updated_at', 'active', 'article',)
    search_fields = ['name']
    list_per_page = 20
    ordering = ['name']

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'sku_number', 'name', 'price', 'type', 'quality', 'image')
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('active', 'type',)
    search_fields = ['sku_number', 'name']
    list_per_page = 20
    ordering = ['name']
    
class ColorAdmin(admin.ModelAdmin):
    model = Color
    list_display = ('active', 'name', 'quality',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', 'quality',)
    
class PatternAdmin(admin.ModelAdmin):
    model = Pattern
    list_display = ('active', 'name', 'quality',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', 'quality',)
 

class SizeAdmin(admin.ModelAdmin):
    model = Size
    
class QualityAdmin(admin.ModelAdmin):
    model = Quality
    list_display = ('active', 'name',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', )

    
class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ('active', 'name',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', )
    
class ImageVariationAdmin(admin.ModelAdmin):
    model = Image
    
    
class ComboAdmin(admin.ModelAdmin):
    model = Image   
    list_display = ('image', 'pattern', 'color','quality',)
    list_display_links = ('image',)
    list_filter = ('quality',)
 
admin.site.register(Variation, VariationAdmin)    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(ImageVariation, ImageVariationAdmin)

admin.site.register(Combo, ComboAdmin)

admin.site.register(CartItem, CartAdmin)    
