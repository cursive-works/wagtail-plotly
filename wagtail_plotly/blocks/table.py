from django import forms
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.table_block.blocks import (
    TableBlock,
    TableInput,
)
from wagtail.core import blocks
from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter


from ..config import (
    DEFAULT_BUBBLE_TABLE_OPTIONS,
)


class PlotTableInput(TableInput):

    @property
    def media(self):
        return super().media + forms.Media(
            css={
                'all': [
                    versioned_static('wagtail_plotly/css/plot_data_table.css'),
                ]
            },
            js=[
                versioned_static('wagtail_plotly/js/plot_data_table.js'),
            ],
        )


class PlotTableInputAdapter(WidgetAdapter):
    js_constructor = 'wagtail_plotly.widgets.PlotTableInput'

    def js_args(self, widget):
        strings = {
            'Table': _('Table'),
        }

        return [
            widget.table_options,
            strings,
        ]


register(PlotTableInputAdapter(), PlotTableInput)


class PlotDataBlock(TableBlock):
    @cached_property
    def field(self):
        return forms.CharField(
            widget=PlotTableInput(table_options=self.table_options),
            **self.field_options,
        )

    def get_searchable_content(self, value):
        return []

    def render(self, value, context=None):
        template = getattr(self.meta, 'template', None)

        if not template or not value:
            return self.render_basic(value or '', context=context)

        new_context = {} if context is None else dict(context)
        new_context.update({'self': value})

        return render_to_string(template, new_context)


class BubblePlotDataBlock(blocks.StructBlock):
    """
    Bubble plot data block
    """
    group_name = blocks.CharBlock(help_text='Name of the bubble group')

    plot_data = PlotDataBlock(
        table_options=DEFAULT_BUBBLE_TABLE_OPTIONS,
        help_text=(
            'Bubble plot data with Name, X, Y and Z values.'
        ),
    )
