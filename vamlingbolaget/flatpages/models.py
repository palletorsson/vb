from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


class Flatpage(FlatPage):
    title_sv = models.CharField(_('title'), max_length=200)
    title_en = models.CharField(_('title'), max_length=200)
    content_sv = models.TextField(_('content'), blank=True)
    content_en = models.TextField(_('content'), blank=True)
