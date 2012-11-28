from modeltranslation.translator import translator, TranslationOptions
from models import Flatpage

class FlatpageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

translator.register(Flatpage, FlatpageTranslationOptions)
