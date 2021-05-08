from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks

from wagtail_color_panel.blocks import NativeColorBlock

from .base import (
    BaseBarChartBlock,
    BaseBubblePlotBlock,
    BaseContourPlotBlock,
    BaseDotPlotBlock,
    BaseHeatmapPlotBlock,
    BaseLinePlotBlock,
    BasePieChartBlock,
    BaseScatterPlotBlock,
    BaseSurfacePlotBlock,
)
from .layout import LayoutChooserBlock


PLOT_FILL_CHOICES = [
    ('none', _('None')),
    ('tozeroy', _('To zero y')),
    ('tozerox', _('To zero x')),
    ('tonexty', _('To next y')),
    ('tonextx', _('To next x')),
    ('toself', _('To self')),
    ('tonext', _('To next')),
]

MODE_CHOICES = [
    ('lines', _('Lines')),
    ('lines+markers', _('Lines and markers')),
    ('markers', _('Markers')),
    ('none', _('None - no lines or markers')),
]

LINE_SHAPE_CHOICES = [
    ('linear', _('Linear')),
    ('spline', _('Spline'))
]


MARKER_SYMBOL_CHOICES = [
    ('circle', _('Circle')),
    ('square', _('Square')),
    ('diamond', _('Diamond')),
    ('cross', _('Cross')),
    ('triangle-up', _('Triangle-up')),
    ('star', _('Star')),
]

MARKER_FILL_CHOICES = [
    ('-open', _('Open')),
    ('-dot', _('Dot')),
    ('-open-dot', _('Open/Dot')),
]

ORIENTATION_CHOICES = [
    ('v', _('Vertical')),
    ('h', _('Horizontal')),
]

BARMODE_CHOICES = [
    ('group', _('Group')),
    ('stack', _('Stack')),
]

COLORSCALE_CHOICES = [
    ('greys', 'Greys'),
    ('ylgnbu', 'YlGnBu'),
    ('greens', 'Greens'),
    ('ylorrd', 'YlOrRd'),
    ('bluered', 'Bluered'),
    ('rdbu', 'RdBu'),
    ('reds', 'Reds'),
    ('blues', 'Blues'),
    ('picnic', 'Picnic'),
    ('rainbow', 'Rainbow'),
    ('portland', 'Portland'),
    ('jet', 'Jet'),
    ('hot', 'Hot'),
    ('blackbody', 'Blackbody'),
    ('earth', 'Earth'),
    ('electric', 'Electric'),
    ('viridis', 'Viridis'),
    ('cividis', 'Cividis'),
]

ZSMOOTH_CHOICES = [
    ('fast', _('Fast')),
    ('best', _('Best')),
]


class BarChartBlock(BaseBarChartBlock):
    """
    Basic bar chart block
    """
    orientation = blocks.ChoiceBlock(
        default='v',
        choices=ORIENTATION_CHOICES,
        help_text='Display as a vertical or horizontal bar chart',
    )

    marker_line_color = NativeColorBlock(
        required=False,
        help_text='Line color for bar chart',
    )

    marker_line_width = blocks.IntegerBlock(
        default=1,
        min_value=0,
        max_value=10,
        help_text='Line width for bar chart',
    )

    barmode = blocks.ChoiceBlock(
        default='group',
        choices=BARMODE_CHOICES,
        help_text='Display as a grouped or stacked bar chart',
    )

    bargroupgap = blocks.FloatBlock(
        default=0.1,
        min_value=0,
        max_value=0.5,
        help_text='Gap between bars of the same location coordinate',
    )

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['orientation', 'marker_line_color', 'marker_line_width']

    def get_layout_fields(self):
        return ['barmode', 'bargroupgap']


class BubblePlotBlock(BaseBubblePlotBlock):
    """
    Basic bubble plot
    """
    layout = LayoutChooserBlock(required=False)


class ContourPlotBlock(BaseContourPlotBlock):
    """
    Basic contour plot
    """
    colorscale = blocks.ChoiceBlock(
        required=False,
        choices=COLORSCALE_CHOICES,
        help_text='Sets the colorscale',
    )

    reversescale = blocks.BooleanBlock(
        required=False,
        help_text='Reverse the colorscale',
    )

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['colorscale', 'reversescale']


class DotPlotBlock(BaseDotPlotBlock):
    """
    Basic dot plot
    """
    marker_size = blocks.IntegerBlock(default=12, min_value=1, max_value=40)

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['marker_size']


class HeatmapPlotBlock(BaseHeatmapPlotBlock):
    """
    Basic heatmap plot
    """
    colorscale = blocks.ChoiceBlock(
        required=False,
        choices=COLORSCALE_CHOICES,
        help_text='Sets the colorscale',
    )

    reversescale = blocks.BooleanBlock(
        required=False,
        help_text='Reverse the colorscale',
    )

    zsmooth = blocks.ChoiceBlock(
        required=False,
        choices=ZSMOOTH_CHOICES,
        help_text='Picks a smoothing algorithm use to smooth z data',
    )

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['colorscale', 'reversescale', 'zsmooth']


class PieChartBlock(BasePieChartBlock):
    """
    Basic pie chart block
    """
    hole = blocks.FloatBlock(
        default=0,
        max_value=0.9,
        min_value=0,
        help_text='Hole size for pie chart',
    )

    marker_line_color = NativeColorBlock(
        required=False,
        help_text='Line color for pie chart',
    )

    marker_line_width = blocks.IntegerBlock(
        default=1,
        min_value=0,
        max_value=10,
        help_text='Line width for pie chart',
    )

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['hole', 'marker_line_color', 'marker_line_width']


class LinePlotBlock(BaseLinePlotBlock):
    """
    Basic line plot with common x axis values
    """
    mode = blocks.ChoiceBlock(default='lines', choices=MODE_CHOICES)
    fill = blocks.ChoiceBlock(default='none', choices=PLOT_FILL_CHOICES)
    line_shape = blocks.ChoiceBlock(default='linear', choices=LINE_SHAPE_CHOICES)
    line_width = blocks.IntegerBlock(default=2, min_value=1, max_value=5)
    marker_size = blocks.IntegerBlock(default=6, min_value=1, max_value=40)

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['mode', 'fill', 'line_shape', 'line_width', 'marker_size']


class ScatterPlotBlock(BaseScatterPlotBlock):
    """
    Basic scatter plot
    """
    mode = blocks.ChoiceBlock(default='markers', choices=MODE_CHOICES)
    fill = blocks.ChoiceBlock(default='none', choices=PLOT_FILL_CHOICES)
    line_shape = blocks.ChoiceBlock(default='linear', choices=LINE_SHAPE_CHOICES)
    line_width = blocks.IntegerBlock(default=2, min_value=1, max_value=5)
    marker_size = blocks.IntegerBlock(default=6, min_value=1, max_value=40)

    marker_symbol = blocks.ChoiceBlock(
        required=False,
        choices=MARKER_SYMBOL_CHOICES,
        help_text='Sets the marker symbol type',
    )

    marker_fill = blocks.ChoiceBlock(
        required=False,
        choices=MARKER_FILL_CHOICES,
        help_text='Sets the marker fill style',
    )

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['mode', 'fill', 'line_shape', 'line_width', 'marker_size', 'marker_symbol']

    def update_traces(self, fig, value):
        super().update_traces(fig, value)

        if value['marker_symbol'] and value['marker_fill']:
            marker_symbol = value['marker_symbol'] + value['marker_fill']
            fig.update_traces(marker_symbol=marker_symbol)


class SurfacePlotBlock(BaseSurfacePlotBlock):
    """
    Basic 3D surface plot
    """
    colorscale = blocks.ChoiceBlock(
        required=False,
        choices=COLORSCALE_CHOICES,
        help_text='Sets the colorscale',
    )

    reversescale = blocks.BooleanBlock(
        required=False,
        help_text='Reverse the colorscale',
    )

    layout = LayoutChooserBlock(required=False)

    def get_trace_fields(self):
        return ['colorscale', 'reversescale']
