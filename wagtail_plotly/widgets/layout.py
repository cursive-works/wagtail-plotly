from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser

from ..models.layout import Layout


class LayoutChooser(AdminChooser):
    choose_one_text = _('Choose a plotly layout')
    choose_another_text = _('Choose another plotly layout')
    model = Layout
    choose_modal_url_name = 'plotly_layout_chooser:choose'
