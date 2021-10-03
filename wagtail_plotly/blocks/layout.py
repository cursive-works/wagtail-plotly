from django.utils.functional import cached_property

from wagtail.core import blocks

from ..widgets.palette import PaletteChooser
from ..widgets.layout import LayoutChooser


class PaletteChooserBlock(blocks.ChooserBlock):
    @cached_property
    def target_model(self):
        return PaletteChooser.model

    @cached_property
    def widget(self):
        return PaletteChooser()

    def get_form_state(self, value):
        return self.widget.get_value_data(value)


class LayoutChooserBlock(blocks.ChooserBlock):
    @cached_property
    def target_model(self):
        return LayoutChooser.model

    @cached_property
    def widget(self):
        return LayoutChooser()

    def get_form_state(self, value):
        return self.widget.get_value_data(value)
