# Wagtail-Plotly

Create charts in Wagtail using Plotly. This is work in progress, so expect breaking changes!

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

from wagtail_plotly.blocks import (
    BarPlotBlock,
    LinePlotBlock,
    PiePlotBlock,
    ScatterPlotBlock,
)

class MyStreamBlock(blocks.StreamBlock):
    line_plot = LinePlotBlock()
    bar_plot = BarPlotBlock()
    pie_plot = PiePlotBlock()
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

## Admin interface

`wagtail-plotly` is installed as a separate items in the Wagtail admin menu. It currently only has two options, Palettes and Layouts.

### Palettes

`Palettes` consist of a selection of colors that are used to draw the plots. Any number of palettes can be created. A user defined `Palette` can be selected in a `Layout` for the `colorway` field.

### Layouts

Layouts control the look, style and positioning of the `wagtail-plotly` plot elements. There are settings for controlling title layout, fonts, legends and margins. More fields need adding to cover all of Plotly's layout options...more will be added.

In the interface for each plot block, it is possible to select a `Layout`

## Plot blocks

There are currently 4 plot blocks available:

* BarPlotBlock
* LinePlotBlock
* PiePlotBlock
* ScatterPlotBlock

Each plot block has a number of fields appropriate to its type. All of the blocks have a `Plot data` field. This is based on the `wagtail.contrib.table_block`.

### Line and bar plots

The data for each plot has to be entered in the table in a specific way, so it can be interpreted correctly. The column and row headers for the `Plot data` table have labels to help with this. For example, to create a plot that tracked the rainfall each month for a range of years, the table might look something like the following:

|          | X       | Y0     | Y1     | Y2     | ...Yn  |
|----------|:-------:|:------:|:------:|:------:|:------:|
| **Name** | `Month` | `2018` | `2019` | `2020` |        |
| **D0**   | Jan     | 3      | 1      | 2.3    |        |
| **D1**   | Feb     | 4.3    | 2.2    | 2      |        |
| **D2**   | Mar     | 5      | 7.9    | 6      |        |
| **D3**   | Apr     | 7      | 8      | 7.2    |        |
| **...**  |         |        |        |        |        |
| **Dn**   |         |        |        |        |        |

With `line` and `bar` plots, the first X column is common. In this instance, D0 to D3 holds the month name. The first row of the table is special in that it holds the names of the data columns. These are used to label the plot traces and legends.

### Scatter plot

A scatter plot `Plot data` is structured with separate X and Y value pairs (X0, Y0), (X1,Y1) etc.

|          | X0          | Y0     | X1       | Y1     |...Xn     | ...Yn  |
|----------|:-----------:|:------:|:--------:|:------:|:--------:|:------:|
| **Name** | `Predicted` | -      | `Actual` | -      |          |        |
| **D0**   | 11          | 3      | 10       | 2.3    |          |        |
| **D1**   | 15          | 4.3    | 16       | 2      |          |        |
| **D2**   | 22          | 5      | 24       | 6      |          |        |
| **D3**   | 19          | 7      | 22       | 7.2    |          |        |
| **...**  |             |        |          |        |          |        |
| **Dn**   |             |        |          |        |          |        |

### Pie chart

This is the most simple table layout, and does not include headers.

| **Name** | **Data** |
|----------|:--------:|
| Jan      | 3        |
| Feb      | 4.3      |
| Mar      | 5        |
| Apr      | 7        |
| ...      |          |
