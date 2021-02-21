# Wagtail-Plotly

Create charts in Wagtail using Plotly. This is work in progress, so expect breaking changes!

![Line plot](docs/img/lineplot.png)
[Some more examples](docs/examples.md)

## Installation

This has not been released to pypi yet, so the easiest way to try it out is to add the following to your requirements.txt:

```
git+git://github.com/cursive-works/wagtail-plotly@master#egg=wagtail-plotly
```

Then add the following to your project's `INSTALLED_APPS`.

```
'wagtail.contrib.table_block',
'generic_chooser',
'wagtail_color_panel',
'wagtail_plotly',
```

## Example use

 One way of using it is to create a `StreamBlock`:

```python
from wagtail.core import blocks

from wagtail_plotly.blocks.plot import (
    BarChartBlock,
    ContourPlotBlock,
    LinePlotBlock,
    PieChartBlock,
    ScatterPlotBlock,
)

class MyStreamBlock(blocks.StreamBlock):
    bar_chart = BarChartBlock()
    contour_plot = ContourPlotBlock()
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


class HomePage(Page):

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

## Data input format

More information about each plot type and input data format can be found in the [docs](docs/plots.md)

## Build your own

The plots in `wagtail-plotly` is based around a set of base block classes, that can be extended to create your own plots. The intention is to allow custom layouts and trace config whilst handling the data input. The base classes are:

* BaseBarChartBlock
* BaseContourPlotBlock
* BaseHeatmapPlotBlock
* BaseLinePlotBlock
* BasePieChartBlock
* BaseScatterPlotBlock

## Admin interface

`wagtail-plotly` is installed as a separate items in the Wagtail admin menu. It currently only has two options, Palettes and Layouts.

### Palettes

`Palettes` consist of a selection of colors that are used to draw the plots. Any number of palettes can be created. A user defined `Palette` can be selected in a `Layout` for the `colorway` field.

### Layouts

Layouts control the look, style and positioning of the `wagtail-plotly` plot elements. There are settings for controlling title layout, fonts, legends and margins. More fields need adding to cover all of Plotly's layout options...more will be added.

In the interface for each plot block, it is possible to select a `Layout`
