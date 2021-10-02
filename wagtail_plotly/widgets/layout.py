from django.utils.translation import gettext_lazy as _

from generic_chooser.widgets import AdminChooser

from ..models.layout import Layout


class LayoutChooser(AdminChooser):
    choose_one_text = _('Choose a plotly layout')
    choose_another_text = _('Choose another plotly layout')
    model = Layout
    choose_modal_url_name = 'plotly_layout_chooser:choose'

    # TODO: How to add edit link
    # link_to_chosen_text = _('Edit this layout')

    # def get_edit_item_url(self, item):
    #     return reverse('wagtailsnippets:edit', args=('base', 'people', quote(item.pk)))
