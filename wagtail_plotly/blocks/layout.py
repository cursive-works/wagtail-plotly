from django.utils.functional import cached_property

from ..widgets.palette import PaletteChooser
from ..widgets.layout import LayoutChooser

from wagtail.core import blocks


class PaletteChooserBlock(blocks.ChooserBlock):
    @cached_property
    def target_model(self):
        return PaletteChooser.model

    @cached_property
    def widget(self):
        return PaletteChooser()


class LayoutChooserBlock(blocks.ChooserBlock):
    @cached_property
    def target_model(self):
        return LayoutChooser.model

    @cached_property
    def widget(self):
        return LayoutChooser()
