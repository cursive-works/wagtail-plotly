

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

SCATTER_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
SCATTER_TABLE_OPTIONS.update(
    {
        'plotType': 'scatter',
    }
)

LINE_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
LINE_TABLE_OPTIONS.update(
    {
        'plotType': 'line',
    }
)

BAR_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
BAR_TABLE_OPTIONS.update(
    {
        'plotType': 'bar',
    }
)

PIE_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
PIE_TABLE_OPTIONS.update(
    {
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
    }
)

CONTOUR_TABLE_OPTIONS = DEFAULT_TABLE_OPTIONS.copy()
CONTOUR_TABLE_OPTIONS.update(
    {
        'plotType': 'contour',
    }
)

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

DEFAULT_CHART_CONFIG = {}
