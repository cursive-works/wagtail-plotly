from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser

from ..models.layout import Layout
from ..wagtail_hooks import LayoutAdmin


class LayoutChooser(AdminChooser):
    choose_one_text = _('Choose a plotly layout')
    choose_another_text = _('Choose another plotly layout')
    link_to_chosen_text = _('Edit this layout')
    model = Layout
    choose_modal_url_name = 'plotly_layout_chooser:choose'

    def get_edit_item_url(self, item):
        return LayoutAdmin().url_helper.get_action_url('edit', item.pk)
