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
    list_display = ('active', 'name', 'article', 'color', 'pattern')
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('created_at', 'updated_at', 'active')

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('active', 'sku_number', 'name', 'price', 'type', 'quality', 'image')
    list_display_links = ('name',)
    list_editable = ('active',)
    list_filter = ('active', )

class ColorAdmin(admin.ModelAdmin):
    model = Color
    list_display = ('active', 'name', )
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', )

    
class PatternAdmin(admin.ModelAdmin):
    model = Pattern
    list_display = ('active', 'name',)
    list_display_links = ('name',)
    list_editable = ('active', )
    list_filter = ('active', )
 

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
    
class ImageAdmin(admin.ModelAdmin):
    model = Image
    
admin.site.register(Variation, VariationAdmin)    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Image, ImageAdmin)