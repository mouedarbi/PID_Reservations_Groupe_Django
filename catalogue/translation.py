from modeltranslation.translator import register, TranslationOptions
from .models.show import Show
from .models.type import Type
from .models.location import Location

@register(Show)
class ShowTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Type)
class TypeTranslationOptions(TranslationOptions):
    fields = ('type',)

@register(Location)
class LocationTranslationOptions(TranslationOptions):
    fields = ('designation',)
