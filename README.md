# Wagtail-Plotly

Create charts in Wagtail using Plotly. This is project is in Alpha, so expect breaking changes!

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
```

## Out of the box

There are currently several plot blocks that are ready to use:

* [BarChartBlock / LinePlotBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/bar_and_line.md)
* [ContourPlotBlock / HeatmapPlotBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/contour_and_heatmap.md)
* [PieChartBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/pie.md)
* [ScatterPlotBlock](https://github.com/cursive-works/wagtail-plotly/blob/master/docs/scatter.md)

Each plot block has a number of trace/layout fields appropriate to its type.

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
Configuring `plotly` graphs *can* be complex. There are A LOT of options available. `plotly` provide [Chart Studio](https://chart-studio.plotly.com) from which graphs and layouts can be made and exported as JSON data. 

`wagtail-plotly` is designed to consume a subset of this data with minimal effort by developers:
`wagtail-plotly` will look for directories named `plotly` in each installed app and any `.json` files therein are assumed to be configuration options that are presented to users as `Graph layout` options. In this way developers can provide managed plot configurations to end-users that override the default settings.

TODO: Document the format of these configuration files. 

The plots in `wagtail-plotly` are based around a set of stream block classes. These can be used as is or extended to create custom plots. The intention is to allow custom layouts and trace config whilst handling the data input. Out of the box `wagtail-plotly` provides:

* BarChartBlock
* ContourPlotBlock
* HeatmapPlotBlock
* LinePlotBlock
* PieChartBlock
* ScatterPlotBlock

Each block class inherits from `BasePlotBlock`. All of the blocks have a `plot_data` field for entering plot data (based on `wagtail.contrib.table_block`) and `build_data` method for extracting data from the table ready for plotting.

### Creating new plot blocks

New plot blocks can be created by inheriting from either`BasePlotBlock` or one of the above blocks.
