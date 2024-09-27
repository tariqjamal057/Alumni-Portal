from django.utils.translation import gettext_lazy as _
from django.db import models

    
class GenderEnum(models.IntegerChoices):
    NOT_PREFER_TO_SAY = 0, _("Not Prefer To Say")
    MALE = 10, _("Male")
    FEMALE = 20, _("Female")
    OTHERS = 30, _("Others")

