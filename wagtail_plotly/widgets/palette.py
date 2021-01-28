from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser

from ..models.palette import Palette


class PaletteChooser(AdminChooser):

    choose_one_text = _('Choose a color palette')
    choose_another_text = _('Choose another color palette')
    model = Palette
    choose_modal_url_name = 'plotly_palette_chooser:choose'
