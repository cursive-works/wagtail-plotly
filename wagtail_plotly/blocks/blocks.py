import plotly.graph_objects as go

from wagtail.core import blocks

from ..config import (
    DEFAULT_BAR_TABLE_OPTIONS,
    DEFAULT_CONTOUR_TABLE_OPTIONS,
    DEFAULT_DOT_TABLE_OPTIONS,
    DEFAULT_LINE_TABLE_OPTIONS,
    DEFAULT_PIE_TABLE_OPTIONS,
    DEFAULT_SCATTER_TABLE_OPTIONS,
)
from .table import (
    BubblePlotDataBlock,
    PlotDataBlock,
)

from .base import BasePlotBlock, CustomPlotMixin

from ..utils import to_float


class BarChartBlock(BasePlotBlock):
    """
    Base bar chart block
    """
    plot_data = PlotDataBlock(
        table_options=DEFAULT_BAR_TABLE_OPTIONS,
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


class ContourPlotBlock(BasePlotBlock):
    """
    Base contour plot block
    """
    plot_class = go.Contour

    plot_data = PlotDataBlock(
        table_options=DEFAULT_CONTOUR_TABLE_OPTIONS,
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


class HeatmapPlotBlock(ContourPlotBlock):
    """
    Base heatmap plot block
    """
    plot_class = go.Heatmap


class SurfacePlotBlock(ContourPlotBlock):
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


class LinePlotBlock(BasePlotBlock):
    """
    Base line plot with common x axis values
    """
    plot_data = PlotDataBlock(
        table_options=DEFAULT_LINE_TABLE_OPTIONS,
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


class PieChartBlock(BasePlotBlock):
    """
    Base pie chart block
    """
    xaxis_title = None
    yaxis_title = None

    plot_data = PlotDataBlock(
        table_options=DEFAULT_PIE_TABLE_OPTIONS,
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


class ScatterPlotBlock(BasePlotBlock):
    """
    Base scatter plot block
    """
    plot_data = PlotDataBlock(
        table_options=DEFAULT_SCATTER_TABLE_OPTIONS,
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


class DotPlotBlock(BasePlotBlock):
    """
    Base dot plot with common y axis values
    """
    plot_data = PlotDataBlock(
        table_options=DEFAULT_DOT_TABLE_OPTIONS,
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


class BubblePlotBlock(BasePlotBlock):
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

    def update_figure(self, fig, value):
        fig.update_traces(marker=dict(sizemode='area', sizeref=self.sizeref, line_width=2))


class CustomBarChartBlock(CustomPlotMixin, BarChartBlock):
    pass
class CustomContourPlotBlock(CustomPlotMixin, ContourPlotBlock):
    pass
class CustomHeatmapPlotBlock(CustomPlotMixin, HeatmapPlotBlock):
    pass
class CustomLinePlotBlock(CustomPlotMixin, LinePlotBlock):
    pass
class CustomPieChartBlock(CustomPlotMixin, PieChartBlock):
    pass
class CustomScatterPlotBlock(CustomPlotMixin, ScatterPlotBlock):
    pass
