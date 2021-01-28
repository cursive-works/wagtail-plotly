from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from .models.palette import Palette
from .models.layout import Layout

from .views import (
    PaletteChooserViewSet,
    LayoutChooserViewSet,
)


@hooks.register('register_admin_viewset')
def register_plotly_palette_chooser_viewset():
    return PaletteChooserViewSet('plotly_palette_chooser', url_prefix='plotly-palette-chooser')


@hooks.register('register_admin_viewset')
def register_plotly_layout_chooser_viewset():
    return LayoutChooserViewSet('plotly_layout_chooser', url_prefix='plotly-layout-chooser')


class PaletteAdmin(ModelAdmin):
    model = Palette
    menu_label = _('Palettes')


class LayoutAdmin(ModelAdmin):
    model = Layout
    menu_label = _('Layouts')


class PlotlyModelAdminGroup(ModelAdminGroup):
    menu_label = _('Plotly')
    items = (PaletteAdmin, LayoutAdmin)


modeladmin_register(PlotlyModelAdminGroup)
