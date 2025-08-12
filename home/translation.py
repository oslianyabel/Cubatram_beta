from modeltranslation.translator import TranslationOptions, register

from .models import Category, Destination, HeroSection, InfoPoint, InfoSection, Tour


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title", "subtitle")


@register(Destination)
class DestinationTranslationOptions(TranslationOptions):
    fields = ("para1", "para2", "para3")


@register(Tour)
class TourTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "description")


@register(InfoSection)
class InfoSectionTranslationOptions(TranslationOptions):
    fields = ("title", "subtitle", "content")


@register(InfoPoint)
class InfoPointTranslationOptions(TranslationOptions):
    fields = ("content",)


@register(HeroSection)
class HeroSectionTranslationOptions(TranslationOptions):
    fields = (
        "title1",
        "title2",
        "title3",
    )
