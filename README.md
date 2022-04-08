# Wagtail Plotly

This project aims to provide *content focused* management of [Plotly.py](https://github.com/plotly/plotly.py) 
charts in [Wagtail CMS](https://wagtail.io) and to give developers and easy way customise and extend plots.

![Line plot](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/img/lineplot.png)
[Some more examples](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/examples.md)

## Installation

Install from [PyPI](https://pypi.org/project/wagtail-plotly/):

```
pip install wagtail-plotly
```

Then add the following to your project's `INSTALLED_APPS`.

```
'wagtail.contrib.table_block',
'wagtail_plotly',
'wagtail_json_widget',
```

## Settings

#### `WAGTAIL_PLOTLY_INCLUDE_PLOTLYJS` 
Default: `'https://cdn.plot.ly/plotly-1.58.4.min.js'`

A url string providing the location of a Plotly JS libarary

#### `DEFAULT_PLOTLY_JSON_DIRECTORY` 
Default: `'plotly'`

The name of the `app` directory in which to look for custom json plots. Wagtail Plotly will search all installed apps looking for a directory matching the `DEFAULT_PLOTLY_JSON_DIRECTORY` value and will attempt to load any `.json` files it contains. [See Customising](#Customising) for more information.  

## Usage overview

There are several plot blocks that you can use out of the box:

* [BarChartBlock / LinePlotBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/bar_and_line.md)
* [ContourPlotBlock / HeatmapPlotBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/contour_and_heatmap.md)
* [PieChartBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/pie.md)
* [ScatterPlotBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/scatter.md)

Adding one of these blocks provides you with input fields to manage the content of your plot, primarily titles and data, and a layout/style option(s). There is one default option out-of-the-box and more can be added by developers via `.json` files using [Plotly's schema](https://plotly.com/python/reference/index/). [See Customising](#Customising)

This app also provides versions of the above blocks that support case by case customisation via a json field in the CMS UI.

### Example use

 One way of using it is to create a `StreamBlock`:

```python
from wagtail.core import blocks

from wagtail_plotly.blocks import (
    BarChartBlock,
    ContourPlotBlock,
    HeatmapPlotBlock,
    LinePlotBlock,
    PieChartBlock,
    ScatterPlotBlock,
)

class MyStreamBlock(blocks.StreamBlock):
    bar_chart = BarChartBlock()
    contour_plot = ContourPlotBlock()
    heatmap_plot = HeatmapPlotBlock()
    line_plot = LinePlotBlock()
    pie_chart = PieChartBlock()
    scatter_plot = ScatterPlotBlock()
```

Add the `StreamBlock` to a `StreamField` on a Wagtail page:

```python
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from .blocks import MyStreamBlock


class MyPage(Page):

    body = StreamField(MyStreamBlock(), null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
```
Then in the page template:

```
{% load static wagtailcore_tags %}

{% include_block page.body %}
```

## Customising
Configuring `plotly` graphs *can* be complex because there are a lot of options available. `plotly` provide [Chart Studio](https://chart-studio.plotly.com) from which graphs and layouts can be made and exported as JSON data. 

Wagtail Plotly is designed to consume a subset of this data with minimal effort by developers:
Wagtail Plotly will look for directories named `plotly` (by default) in each installed app and any `.json` files therein are assumed to be configuration options that are presented to users as `Graph layout` options. In this way developers can provide managed plot configurations to end-users that override the default settings.

For example: `my_plot.json` might contain:
```json
{
    "layout": {
        "xaxis": {
            "gridcolor": "#dddddd",
            "mirror": true
        },
        "yaxis": {
            "gridcolor": "#dddddd",
            "mirror": true
        },
        "autosize": true,
        "colorway": [
            "#4c78a8",
            "#f58518",
            "#e45756",
            "#72b7b2",
            "#54a24b",
            "#eeca3b",
            "#b279a2",
            "#ff9da6",
            "#9d755d",
            "#bab0ac"
        ]
    }
}
```

### Customising StreamField Blocks

Plots in Wagtail Plotly are a set of Wagtail StreamField blocks that share a common base `BasePlotBlock`. They can be used as is or extended to create custom plots or features of Plotly that aren't (yet) handled by default. 

All of the blocks have a `plot_data` field for entering plot data (based on `wagtail.contrib.table_block`) and `build_data` method for extracting data from the table ready for plotting.

### Creating new plot blocks

New plot blocks can be created in the usual way: subclassing from either`BasePlotBlock` or one of the above blocks.
