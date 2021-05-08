import json

from django import forms
from django.template.loader import render_to_string
from django.utils.functional import cached_property

from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks

from ..config import (
    BUBBLE_TABLE_OPTIONS,
)


class PlotTableInput(forms.HiddenInput):
    template_name = 'wagtail_plotly/widgets/plot_data_table.html'

    def __init__(self, table_options=None, attrs=None):
        self.table_options = table_options
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context['widget']['table_options_json'] = json.dumps(self.table_options)
        return context


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


class BubblePlotDataBlock(blocks.StructBlock):
    """
    Bubble plot data block
    """
    group_name = blocks.CharBlock(help_text='Name of the bubble group')

    plot_data = PlotDataBlock(
        table_options=BUBBLE_TABLE_OPTIONS,
        help_text=(
            'Bubble plot data with Name, X, Y and Z values.'
        ),
    )
