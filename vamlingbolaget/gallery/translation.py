from modeltranslation.translator import translator, TranslationOptions
from models import *

class ImageTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Image, ImageTranslationOptions)

class GalleryTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Gallery, GalleryTranslationOptions)

class GalleryStatusTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(GalleryStatus, GalleryStatusTranslationOptions)
