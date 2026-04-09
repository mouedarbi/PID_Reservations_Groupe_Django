from modeltranslation.translator import register, TranslationOptions
from .models.show import Show
from .models.type import Type
from .models.location import Location
from .models.price import Price
from .models.locality import Locality

@register(Show)
class ShowTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Type)
class TypeTranslationOptions(TranslationOptions):
    fields = ('type',)

@register(Location)
class LocationTranslationOptions(TranslationOptions):
    fields = ('designation', 'address')

@register(Price)
class PriceTranslationOptions(TranslationOptions):
    fields = ('type', 'description')

@register(Locality)
class LocalityTranslationOptions(TranslationOptions):
    fields = ('locality',)
