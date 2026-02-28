from modeltranslation.translator import translator, TranslationOptions
from .models import Property


class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'location')


translator.register(Property, PropertyTranslationOptions)
