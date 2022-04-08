from django.conf import settings


# Include specific version of plotly js from CDN.
# See plotly documentation for other settings, .e.g 'cdn' or False
DEFAULT_INCLUDE_PLOTLYJS = 'https://cdn.plot.ly/plotly-1.58.4.min.js'
INCLUDE_PLOTLYJS = getattr(settings, 'WAGTAIL_PLOTLY_INCLUDE_PLOTLYJS', DEFAULT_INCLUDE_PLOTLYJS)

DEFAULT_PLOTLY_JSON_DIRECTORY = 'plotly'
PLOTLY_FIGURE_DIRECTORY = getattr(settings, 'WAGTAIL_PLOTLY_JSON_DIRECTORY', DEFAULT_PLOTLY_JSON_DIRECTORY)

DEFAULT_TRACE_OPTIONS = {}

#
# Data tables
#

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
        'cut',
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 240,
    'renderer': 'text',
    'autoColumnSize': False,
}

TABLE_OPTIONS = getattr(settings, 'WAGTAIL_PLOTLY_TABLE_OPTIONS', DEFAULT_TABLE_OPTIONS)


DEFAULT_BAR_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_BAR_TABLE_OPTIONS.update(
    {
        'plotType': 'bar',
    }
)

DEFAULT_BUBBLE_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_BUBBLE_TABLE_OPTIONS.update(
    {
        'plotType': 'bubble',
        'colHeaders': ['Name', 'X', 'Y', 'Z'],
        'startCols': 4,
        'startRows': 5,
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
        'height': 160,
    }
)

DEFAULT_CONTOUR_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_CONTOUR_TABLE_OPTIONS.update(
    {
        'plotType': 'contour',
    }
)

DEFAULT_DOT_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_DOT_TABLE_OPTIONS.update(
    {
        'plotType': 'dot',
    }
)

DEFAULT_LINE_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_LINE_TABLE_OPTIONS.update(
    {
        'plotType': 'line',
    }
)

DEFAULT_PIE_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_PIE_TABLE_OPTIONS.update(
    {
        'plotType': 'pie',
        'colHeaders': ['Name', 'Value'],
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
    }
)


DEFAULT_SCATTER_TABLE_OPTIONS = TABLE_OPTIONS.copy()
DEFAULT_SCATTER_TABLE_OPTIONS.update(
    {
        'plotType': 'scatter',
    }
)

#
# Plot settings, config, layout and traces
#

DEFAULT_CONFIG_OPTIONS = {
    'displayModeBar': False,
}

DEFAULT_LAYOUT_OPTIONS = {
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
    'margin': {'t': 80, 'b': 20, 'l': 20, 'r': 20},
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
    },
}
