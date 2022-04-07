import json
import plotly.graph_objects as go

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.core import blocks
from wagtail_json_widget.blocks import JSONBlock

from ..config import (
    DEFAULT_CONFIG_OPTIONS,
    DEFAULT_LAYOUT_OPTIONS,
    DEFAULT_TRACE_OPTIONS,
    INCLUDE_PLOTLYJS,
)

from ..utils import (
    get_layout, 
    get_config, 
    get_trace, 
    get_layout_choices
)


class BasePlotBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=False)
    xaxis_title = blocks.CharBlock(required=False)
    yaxis_title = blocks.CharBlock(required=False)
    graph_layout = blocks.ChoiceBlock(required=False, choices=get_layout_choices)

    def get_rows(self, plot_data):
        """
        Get the rows from the table removing empty rows
        """
        return [row for row in plot_data if any(row)]

    def get_columns(self, plot_data):
        """
        Get the data from the table, transpose and filter
        """
        columns = list(zip(*plot_data)) if plot_data else []

        # Remove empty columns
        columns = [column for column in columns if any(column)]

        return columns

    def build_figure(self, data, layout, value):
        """
        Buld the figure from the data and layout and set axis labels
        """
        fig = go.Figure(
            data=data,
            layout=layout,
        )

        fig.update_layout(
            title=value.get('title', ''),
            xaxis_title=value.get('xaxis_title', ''),
            yaxis_title=value.get('yaxis_title', ''),
        )
        return fig

    def fig_to_html(self, fig, config_options):
        """
        Generate the markup for the plot
        """
        return mark_safe(
            fig.to_html(
                full_html=False,
                include_plotlyjs=INCLUDE_PLOTLYJS,
                config=config_options,
            )
        )

    def build_data(self, value):
        raise NotImplementedError('To be implemented in child class')

    def update_figure(self, fig, value):
        """
        An opportunity for subclasses to modify the figure after
        all other configurations have been applied.
        """
        return

    def render(self, value, context=None):
        """
        General render method for each plot
        """
        template = getattr(self.meta, 'template', None)

        if not template or not value:
            return self.render_basic(value or '', context=context)

        data = self.build_data(value)
        # Create a layout traces with layout options provided or default
        graph_layout = value.get('graph_layout')
        layout_options = get_layout(graph_layout) or DEFAULT_LAYOUT_OPTIONS
        config_options = get_config(graph_layout) or DEFAULT_CONFIG_OPTIONS
        trace_options = get_trace(graph_layout) or DEFAULT_TRACE_OPTIONS

        layout = go.Layout(**layout_options)

        fig = self.build_figure(data, layout, value)
        fig.update_traces(**trace_options)

        self.update_figure(fig, value)

        plot = self.fig_to_html(fig, config_options)

        ctx = {} if context is None else dict(context)
        ctx.update({'plot': plot})

        return render_to_string(template, ctx)

    class Meta:
        template = 'wagtail_plotly/blocks/plot.html'
        icon = 'table'


class CustomPlotMixin(blocks.StructBlock):
 
    custom = JSONBlock(required=False)

    def update_figure(self, fig, value):
        ob = self.get_custom_data(value)
        fig.update_layout(**ob.get('layout', {}))
        fig.update_traces(**ob.get('trace', {}))

    def get_custom_data(self, value):
        """
        Return a dict of the custom plotly data
        """
        return json.loads(value['custom'])
