from django.utils.translation import gettext_lazy as _

from generic_chooser.views import ModelChooserViewSet

from .models.palette import Palette
from .models.layout import Layout


class PaletteChooserViewSet(ModelChooserViewSet):
    icon = 'grip'
    model = Palette
    page_title = _("Choose a color palette")
    per_page = 10
    order_by = 'title'


class LayoutChooserViewSet(ModelChooserViewSet):
    icon = 'form'
    model = Layout
    page_title = _("Choose a plotly layout")
    per_page = 10
    order_by = 'title'
