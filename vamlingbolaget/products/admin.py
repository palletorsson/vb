from django.contrib import admin
from models import *



class VariationImageInline(admin.StackedInline):
  model = Image
  max_num=4
  extra=0

class VariationAdmin(admin.ModelAdmin):
    model = Variation
    inlines = [VariationImageInline,]


class ArticleAdmin(admin.ModelAdmin):
    model = Article

class ColorAdmin(admin.ModelAdmin):
    model = Color
    
class PatternAdmin(admin.ModelAdmin):
    model = Pattern
    

class SizeAdmin(admin.ModelAdmin):
    model = Size
    
class QualityAdmin(admin.ModelAdmin):
    model = Quality

class TypeAdmin(admin.ModelAdmin):
    model = Type
    
admin.site.register(Variation, VariationAdmin)    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(Type, TypeAdmin)