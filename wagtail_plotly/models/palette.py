from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
)

from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable

from modelcluster.fields import (
    ParentalKey,
)

from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField


class Color(Orderable):
    palette = ParentalKey('wagtail_plotly.Palette', related_name='colors')
    color = ColorField()

    panels = [
        NativeColorPanel('color')
    ]


class Palette(ClusterableModel):

    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
        InlinePanel('colors', label="Colors"),
    ]

    def values(self):
        return list(self.colors.values_list('color', flat=True))

    def __str__(self):
        return self.title
