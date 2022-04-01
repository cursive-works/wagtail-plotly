import plotly.graph_objects as go

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.core import blocks

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

    def get_trace_fields(self):
        """
        To be implemented in child class for trace fields to be updated
        """
        return []

    def get_layout_fields(self):
        """
        To be implemented in child class for layout fields to be updated
        """
        return []

    def update_traces(self, fig, value):
        """
        Update the traces with config values from the block
        """
        fields = self.get_trace_fields()
        if fields:
            config = {k: v for k, v in value.items() if v != '' and k in fields}
            fig.update_traces(**config)

    def update_layout(self, fig, value):
        """
        Update the layout with values from the block. If a layout model field
        exists it is used, along with any additional fields.
        """
        layout = value.get('layout')
        if layout:
            fig.update_layout(**layout.to_dict())

        fields = self.get_layout_fields()
        if fields:
            config = {k: v for k, v in value.items() if v != '' and k in fields}
            fig.update_layout(**config)

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

        # Update traces with trace options provided or default
        fig.update_traces(**trace_options)

        # Update the traces with any custom options
        self.update_traces(fig, value)

        # Update the layout with any custom options
        # self.update_layout(fig, value)

        plot = self.fig_to_html(fig, config_options)

        ctx = {} if context is None else dict(context)
        ctx.update({'plot': plot})

        return render_to_string(template, ctx)

    class Meta:
        template = 'wagtail_plotly/blocks/plot.html'
        icon = 'table'

