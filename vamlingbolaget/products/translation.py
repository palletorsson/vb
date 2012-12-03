from modeltranslation.translator import translator, TranslationOptions
from models import Article, Type, Quality, Color, Pattern, Category

class ArticleTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Article, ArticleTranslationOptions)

class TypeTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Type, TypeTranslationOptions)

class QualityTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Quality, QualityTranslationOptions)

class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Color, ColorTranslationOptions)

class PatternTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Pattern, PatternTranslationOptions)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)
