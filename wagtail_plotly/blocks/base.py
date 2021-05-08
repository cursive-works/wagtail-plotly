import copy

import plotly.graph_objects as go

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.core import blocks

from ..config import (
    BAR_TABLE_OPTIONS,
    CONFIG_OPTIONS,
    CONTOUR_TABLE_OPTIONS,
    DOT_TABLE_OPTIONS,
    INCLUDE_PLOTLYJS,
    LAYOUT_OPTIONS,
    LINE_TABLE_OPTIONS,
    PIE_TABLE_OPTIONS,
    SCATTER_TABLE_OPTIONS,
    TRACE_OPTIONS,
)
from .table import (
    BubblePlotDataBlock,
    PlotDataBlock,
)


def to_float(value):
    try:
        n = float(value)
    except ValueError:
        n = float('NaN')
    return n


class BasePlotBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=False)
    xaxis_title = blocks.CharBlock(required=False)
    yaxis_title = blocks.CharBlock(required=False)

    def __init__(self, config_options=None, layout_options=None, trace_options=None, **kwargs):

        self.config_options = copy.deepcopy(config_options if config_options else CONFIG_OPTIONS)
        self.layout_options = copy.deepcopy(layout_options if layout_options else LAYOUT_OPTIONS)
        self.trace_options = copy.deepcopy(trace_options if trace_options else TRACE_OPTIONS)
        super().__init__(**kwargs)

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

    def fig_to_html(self, fig):
        """
        Generate the markup for the plot
        """
        return mark_safe(
            fig.to_html(
                full_html=False,
                include_plotlyjs=INCLUDE_PLOTLYJS,
                config=self.config_options,
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
        layout = go.Layout(**self.layout_options)

        fig = self.build_figure(data, layout, value)

        # Update traces with trace options provided or default
        if self.trace_options:
            fig.update_traces(**self.trace_options)

        # Update the traces with any custom options
        self.update_traces(fig, value)

        # Update the layout with any custom options
        self.update_layout(fig, value)

        plot = self.fig_to_html(fig)

        ctx = {} if context is None else dict(context)
        ctx.update({'plot': plot})

        return render_to_string(template, ctx)

    class Meta:
        template = 'wagtail_plotly/blocks/plot.html'
        icon = 'table'


class BaseBarChartBlock(BasePlotBlock):
    """
    Base bar chart block
    """
    plot_data = PlotDataBlock(
        table_options=BAR_TABLE_OPTIONS,
        help_text=(
            'Bar plot data with a set of common X values and multiple sets of Y values. '
            'First row contains Name(s) for legend.'
        ),
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
            x_vals = columns.pop(0)[1:]

            for column in columns:
                x = x_vals
                y = column[1:]

                # Handle horizontal bars by swapping x and y
                if value.get('orientation') == 'h':
                    x, y = y, x

                data.append(
                    go.Bar(name=column[0], x=x, y=y)
                )
        return data


class BaseContourPlotBlock(BasePlotBlock):
    """
    Base contour plot block
    """
    plot_class = go.Contour

    plot_data = PlotDataBlock(
        table_options=CONTOUR_TABLE_OPTIONS,
        help_text=(
            'Contour plot data with X and Y dimensions, with a grid of values representing Z'
        ),
    )

    # TODO: Write some tests for this
    def rstrip(self, row):
        """
        Remove empty and None values from the end of a row of data
        """
        count = 0

        for v in reversed(row):
            if v or v == 0:
                break
            count += 1

        if count > 0:
            return row[:-count]

        return row

    # TODO: Write some tests for this
    def extract_values(self, plot_data):
        """
        Extract x, y and z values from plot data table values
        """
        x = []
        y = []
        z = []

        for i, row in enumerate(plot_data):
            if i == 0:
                x = self.rstrip(row[1:])
            else:
                row_values = self.rstrip(row[1:])

                if row_values:
                    y.append(row[0])
                    z.append(row_values)

        y = self.rstrip(y)

        return x, y, z

    def build_data(self, value):
        """
        Build contour plot data
        """
        plot_data = value['plot_data']

        if not plot_data:
            return []

        x, y, z = self.extract_values(plot_data)

        if x and y:
            data = [self.plot_class(x=y, y=x, z=z)]
        else:
            data = [self.plot_class(z=z)]

        return data


class BaseHeatmapPlotBlock(BaseContourPlotBlock):
    """
    Base heatmap plot block
    """
    plot_class = go.Heatmap


class BaseSurfacePlotBlock(BaseContourPlotBlock):
    """
    Base 3D surface plot block
    """
    plot_class = go.Surface

    def extract_values(self, plot_data):
        x, y, z = super().extract_values(plot_data)

        # Handle non numeric values in surface plots by converting all values to
        # float or NaNs.
        z = [[to_float(value) for value in row] for row in z]
        return x, y, z


class BaseLinePlotBlock(BasePlotBlock):
    """
    Base line plot with common x axis values
    """
    plot_data = PlotDataBlock(
        table_options=LINE_TABLE_OPTIONS,
        help_text=(
            'Line plot data with a set of common X values and multiple sets of Y values. '
            'First row contains Name(s) for legend.'
        ),
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
                    go.Scatter(name=column[0], x=x[1:], y=column[1:])
                )
        return data


class BasePieChartBlock(BasePlotBlock):
    """
    Base pie chart block
    """
    xaxis_title = None
    yaxis_title = None

    plot_data = PlotDataBlock(
        table_options=PIE_TABLE_OPTIONS,
        help_text=(
            'Pie chart data with a set of name and value columns.'
        ),
    )

    def build_data(self, value):
        """
        Build pie plot data
        """
        data = []

        columns = self.get_columns(value['plot_data'])

        if len(columns) >= 2:

            labels = columns[0]
            values = columns[1]

            data = [
                go.Pie(labels=labels, values=values)
            ]
        return data


class BaseScatterPlotBlock(BasePlotBlock):
    """
    Base scatter plot block
    """
    plot_data = PlotDataBlock(
        table_options=SCATTER_TABLE_OPTIONS,
        help_text=(
            'Scatter plot data with multiple sets of X and Y values (X0, Y0), (X1, Y1) etc. '
            'First row contains Name(s) for legend.'
        ),
    )

    def grouped(self, iterable, n):
        return zip(*[iter(iterable)] * n)

    def build_data(self, value):
        """
        Build scatter plot data
        """
        data = []

        # Get the data in column format from the table
        columns = self.get_columns(value['plot_data'])

        groups = list(self.grouped(columns, 2))

        if len(groups) >= 1:
            for group in groups:
                data.append(
                    go.Scatter(name=group[0][0], x=group[0][1:], y=group[1][1:])
                )
        return data


class BaseDotPlotBlock(BasePlotBlock):
    """
    Base dot plot with common y axis values
    """
    plot_data = PlotDataBlock(
        table_options=DOT_TABLE_OPTIONS,
        help_text=(
            'Dot plot data with a set of common Y values and multiple sets of X values. '
            'First row contains Name(s) for legend.'
        ),
    )

    def build_data(self, value):
        """
        Build line plot data
        """
        data = []

        # Get the data in column format from the table
        columns = self.get_columns(value['plot_data'])

        if len(columns) >= 2:
            # Pop the first column for common y values
            y = columns.pop(0)

            for column in columns:
                data.append(
                    go.Scatter(
                        name=column[0],
                        x=column[1:],
                        y=y[1:],
                        mode='markers',
                    )
                )
            return data


class BaseBubblePlotBlock(BasePlotBlock):
    """
    Base bubble plot block
    """
    zaxis_title = blocks.CharBlock(required=False)
    marker_sizemin = blocks.IntegerBlock(default=10, min_value=1, max_value=50)
    max_marker_size = blocks.IntegerBlock(default=100, min_value=1, max_value=200)

    plot_tables = blocks.ListBlock(BubblePlotDataBlock())

    def build_data(self, value):
        """
        Build bubble plot data
        """
        data = []
        marker_sizes = []

        xaxis_title = value['xaxis_title']
        yaxis_title = value['yaxis_title']
        zaxis_title = value['zaxis_title']

        marker_sizemin = value['marker_sizemin']

        plot_tables = value['plot_tables']

        for table in plot_tables:
            group_name = table['group_name']

            # Remove empty rows
            rows = self.get_rows(table['plot_data'])

            # Transform to columns
            columns = self.get_columns(rows)

            # Get list of sizes
            size = columns[3]

            hovertemplate = [
                (
                    f'<b>{row[0]} ({group_name})</b><br>'
                    f'{xaxis_title}: {row[1]}<br>'
                    f'{yaxis_title}: {row[2]}<br>'
                    f'{zaxis_title}: {row[3]}<extra></extra>'
                ) for row in rows
            ]

            data.append(
                go.Scatter(
                    name=group_name,
                    x=columns[1],
                    y=columns[2],
                    marker=dict(
                        size=size,
                    ),
                    mode='markers',
                    hovertemplate=hovertemplate,
                    marker_sizemin=marker_sizemin,
                )
            )
            marker_sizes.append(max(size))

        self.sizeref = 2 * max(marker_sizes) / (value['max_marker_size'] ** 2)

        return data

    def update_traces(self, fig, value):
        super().update_traces(fig, value)

        fig.update_traces(marker=dict(sizemode='area', sizeref=self.sizeref, line_width=2))
