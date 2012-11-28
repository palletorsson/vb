from models import Page
from modeltranslation.translator import translator, TranslationOptions


class FlatpageTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)

translator.register(Page, FlatpageTranslationOptions)

