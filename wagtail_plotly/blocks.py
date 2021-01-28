import json

import plotly.graph_objects as go

from itertools import cycle

from django import forms
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from wagtail.admin.staticfiles import versioned_static
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks

from .widgets.palette import PaletteChooser
from .widgets.layout import LayoutChooser


PLOT_FILL_CHOICES = [
    ('none', 'None'),
    ('tozeroy', 'To zero y'),
    ('tozerox', 'To zero x'),
    ('tonexty', 'To next y'),
    ('tonextx', 'To next x'),
    ('toself', 'To self'),
    ('tonext', 'To next'),
]

DEFAULT_CHART_COLOURS = [
    '#2f4b7c',
    '#00629b',
    '#3c77ab',
    '#665191',
    '#a05195',
    '#d45087',
    '#f95d6a',
    '#ff7c43',
    '#ffa600',
]

DEFAULT_CHART_COLOURS.reverse()

DEFAULT_TABLE_OPTIONS = {
    'minSpareRows': 0,
    'startRows': 10,
    'startCols': 10,
    'colHeaders': True,
    'rowHeaders': True,
    'colWidths': 50,
    'manualColumnMove': False,
    'manualRowMove': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo',
        '---------',
        'copy',
        'cut'
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 240,
    'renderer': 'text',
    'autoColumnSize': False,
}

SCATTER_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
SCATTER_TABLE_OPTIONS.update({
    'plotType': 'scatter',
})

LINE_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
LINE_TABLE_OPTIONS.update({
    'plotType': 'line',
})

BAR_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
BAR_TABLE_OPTIONS.update({
    'plotType': 'bar',
})

PIE_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
PIE_TABLE_OPTIONS.update({
    'plotType': 'pie',
    'colHeaders': ['Name', 'Data'],
    'rowHeaders': False,
    'startCols': 2,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'remove_row',
        '---------',
        'undo',
        'redo',
        '---------',
        'copy',
        'cut',
    ],
})


DEFAULT_CHART_LAYOUT = {
    'autosize': True,
    'legend': {
        'orientation': 'h',
        'y': -0.25,
        'xanchor': 'center',
        'x': 0.5,
    },
    'font': {
        'size': 13,
    },
    'margin': {
        't': 80,
        'b': 20,
        'l': 20,
        'r': 20
    },
    'hoverlabel': {
        'bgcolor': 'white',
        'font': {
            'color': 'black',
            'size': 13,
        },
        'bordercolor': '#eeeeee',
    },
    'plot_bgcolor': '#fefefe',
    'xaxis': {
        'gridcolor': '#eeeeee',
        'ticks': 'outside',
        'showline': True,
        'linecolor': '#aaaaaa',
        'mirror': True,
    },
    'yaxis': {
        'gridcolor': '#eeeeee',
        'ticks': 'outside',
        'showline': True,
        'linecolor': '#aaaaaa',
        'mirror': True,
        'zeroline': False,
    }
}

DEFAULT_CHART_CONFIG = {
    'showlegend': True,
}


class PlotTableInput(forms.HiddenInput):
    template_name = "wagtail_plotly/widgets/plot_data_table.html"

    def __init__(self, table_options=None, attrs=None):
        self.table_options = table_options
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context['widget']['table_options_json'] = json.dumps(self.table_options)
        return context


class PaletteChooserBlock(blocks.ChooserBlock):

    @cached_property
    def target_model(self):
        return PaletteChooser.model

    @cached_property
    def widget(self):
        return PaletteChooser()


class LayoutChooserBlock(blocks.ChooserBlock):

    @cached_property
    def target_model(self):
        return LayoutChooser.model

    @cached_property
    def widget(self):
        return LayoutChooser()


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
            return self.render_basic(value or "", context=context)

        new_context = {} if context is None else dict(context)
        new_context.update({'self': value})
        return render_to_string(template, new_context)

    @property
    def media(self):
        return super().media + forms.Media(
            css={'all': [
                versioned_static('wagtail_plotly/css/plot_data_table.css'),
            ]},
            js=[
                versioned_static('wagtail_plotly/js/plot_data_table.js'),
            ]
        )


class BasePlotBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=False)
    xaxis_title = blocks.CharBlock(required=False)
    yaxis_title = blocks.CharBlock(required=False)

    layout = LayoutChooserBlock(required=False)

    def __init__(self, layout_options=None, config_options=None, **kwargs):
        self.layout_options = layout_options
        self.config_options = config_options
        super().__init__(**kwargs)

    def get_columns(self, plot_data):
        """
        Get the data from the table, transpose and filter
        """
        columns = list(zip(*plot_data)) if plot_data else []

        # Remove empty columns
        columns = [column for column in columns if set(column) != {None}]

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
            yaxis_title=value.get('yaxis_title', '')
        )
        return fig

    def fig_to_html(self, fig):
        """
        Generate the markup for the plot
        """
        # TODO: Make the plotlyjs configurable
        return mark_safe(fig.to_html(
            full_html=False,
            include_plotlyjs='https://cdn.plot.ly/plotly-1.58.4.min.js',
            config={
                'displayModeBar': False,
            }
        ))

    def build_data(self, value):
        raise NotImplementedError('To be implemented in child class')

    def update_layout(self, fig, value):
        """
        Update the layout with values from a layout model
        """
        layout = value.get('layout')

        if layout:
            data = layout.to_dict()
            fig.update_layout(**data)

    def render(self, value, context=None):
        """
        General render method for each plot
        """
        template = getattr(self.meta, 'template', None)

        if not template or not value:
            return self.render_basic(value or "", context=context)

        data = self.build_data(value)

        layout = go.Layout(**self.layout_options) if self.layout_options else go.Layout(**DEFAULT_CHART_LAYOUT)

        fig = self.build_figure(data, layout, value)

        # Update the layout with any custom options
        self.update_layout(fig, value)

        plot = self.fig_to_html(fig)

        ctx = {} if context is None else dict(context)
        ctx.update({'plot': plot})

        return render_to_string(template, ctx)

    class Meta:
        template = 'wagtail_plotly/blocks/plot.html'
        icon = 'table'


class LinePlotBlock(BasePlotBlock):
    """
    Basic line plot with common x axis values
    """
    mode = blocks.ChoiceBlock(
        default='lines',
        choices=[
            ('lines', 'Lines'),
            ('lines+markers', 'Lines and markers'),
            ('markers', 'Markers'),
            ('none', 'None - no lines or markers'),
        ],
    )
    line_shape = blocks.ChoiceBlock(
        default='linear',
        choices=[('linear', 'Linear'), ('spline', 'Spline'), ('hv', 'HV')],
    )
    line_width = blocks.IntegerBlock(default=2, min_value=1, max_value=5)
    marker_size = blocks.IntegerBlock(default=6, min_value=1, max_value=40)
    fill = blocks.ChoiceBlock(
        default='none',
        choices=PLOT_FILL_CHOICES,
    )

    plot_data = PlotDataBlock(
        table_options=LINE_TABLE_OPTIONS,
        help_text=(
            'Line plot data with a set of common X values and multiple sets of Y values. '
            'First row contains Name(s) for legend.'
        )
    )

    def build_data(self, value):
        """
        Build line plot data
        """
        data = []

        # Get the data in column format from the table
        columns = self.get_columns(value['plot_data'])

        if len(columns) >= 2:
            # Pop the first column for common x values
            x = columns.pop(0)

            for column in columns:
                data.append(
                    go.Scatter(
                        name=column[0],
                        x=x[1:],
                        y=column[1:],
                        **DEFAULT_CHART_CONFIG,
                        mode=value['mode'],
                        line_shape=value['line_shape'],
                        line_width=value['line_width'],
                        marker_size=value['marker_size'],
                        fill=value['fill'],
                    )
                )

        return data


class ScatterPlotBlock(BasePlotBlock):
    """
    Scatter plot
    """
    mode = blocks.ChoiceBlock(
        default='markers',
        choices=[
            ('lines', 'Lines'),
            ('lines+markers', 'Lines and markers'),
            ('markers', 'Markers'),
            ('none', 'None - no lines or markers'),
        ],
    )
    line_shape = blocks.ChoiceBlock(
        default='linear',
        choices=[('linear', 'Linear'), ('spline', 'Spline'), ('hv', 'HV')],
    )
    line_width = blocks.IntegerBlock(default=2, min_value=1, max_value=5)
    marker_size = blocks.IntegerBlock(default=6, min_value=1, max_value=40)
    fill = blocks.ChoiceBlock(
        default='none',
        choices=PLOT_FILL_CHOICES,
    )

    plot_data = PlotDataBlock(
        table_options=SCATTER_TABLE_OPTIONS,
        help_text=(
            'Scatter plot data with multiple sets of X and Y values (X0, Y0), (X1, Y1) etc. '
            'First row contains Name(s) for legend.'
        )
    )

    def grouped(self, iterable, n):
        return zip(*[iter(iterable)]*n)

    def build_data(self, value):
        """
        Build scatter plot data
        """
        data = []

        # Get the data in column format from the table
        columns = self.get_columns(value['plot_data'])

        groups = list(self.grouped(columns, 2))

        config = self.config_options if self.config_options else DEFAULT_CHART_CONFIG

        if len(groups) >= 1:
            for group in groups:
                data.append(
                    go.Scatter(
                        name=group[0][0],
                        x=group[0][1:],
                        y=group[1][1:],
                        mode=value['mode'],
                        line_shape=value['line_shape'],
                        line_width=value['line_width'],
                        marker_size=value['marker_size'],
                        fill=value['fill'],
                        **config,
                    )
                )

        return data


class BarPlotBlock(BasePlotBlock):

    stacked = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Display as a stacked bar chart',
    )

    plot_data = PlotDataBlock(
        table_options=BAR_TABLE_OPTIONS,
        help_text=(
            'Bar plot data with a set of common X values and multiple sets of Y values. '
            'First row contains Name(s) for legend.'
        )
    )

    def build_data(self, value):
        """
        Build bar plot data
        """
        data = []

        # Get the data in column format from the table
        columns = self.get_columns(value['plot_data'])

        if len(columns) >= 2:
            # Pop the first column for common x values
            x = columns.pop(0)

            for column in columns:
                data.append(
                    go.Bar(
                        name=column[0],
                        x=x[1:],
                        y=column[1:],
                        **DEFAULT_CHART_CONFIG,
                    )
                )

        return data

    def update_layout(self, fig, value):
        """
        Update the layout after building the figure
        """
        super().update_layout(fig, value)

        fig.update_layout(
            barmode='stack' if value['stacked'] else 'group'
        )


class PiePlotBlock(BasePlotBlock):

    xaxis_title = None
    yaxis_title = None

    donut = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='Display as a donut chart',
    )

    plot_data = PlotDataBlock(
        table_options=PIE_TABLE_OPTIONS,
        help_text='',
    )

    def build_data(self, value):
        """
        Build bar plot data
        """
        data = []

        columns = self.get_columns(value['plot_data'])

        if len(columns) >= 2:

            labels = columns[0]
            values = columns[1]

            data = [
                go.Pie(
                    labels=labels,
                    values=values,
                    **DEFAULT_CHART_CONFIG,
                    hole=0.35 if value['donut'] else 0,
                    marker_line_color='white',
                    marker_line_width=1,
                )
            ]

        return data
