from modeltranslation.translator import register, TranslationOptions
from .models.show import Show
from .models.type import Type
from .models.location import Location
from .models.price import Price
from .models.locality import Locality
from .models.review import Review
from .models.press_article import PressArticle

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

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('review',)

@register(PressArticle)
class PressArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'content')
