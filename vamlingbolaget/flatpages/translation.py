from modeltranslation.translator import translator, TranslationOptions
from django.contrib.flatpages.models import FlatPage


class FlatpageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

translator.register(FlatPage, FlatpageTranslationOptions)
