from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderEnum(models.IntegerChoices):
    NOT_PREFER_TO_SAY = 0, _("Not Prefer To Say")
    MALE = 10, _("Male")
    FEMALE = 20, _("Female")
    OTHERS = 30, _("Others")


class YearChoices(models.IntegerChoices):
    FIRST = 1, _("1st Year")
    SECOND = 2, _("2nd Year")
    THIRD = 3, _("3rd Year")
    FOURTH = 4, _("4th Year")
    FIFTH = 5, _("5th Year")
    SIXTH = 6, _("6th Year")
    SEVENTH = 7, _("7th Year")
    EIGHTH = 8, _("8th Year")
