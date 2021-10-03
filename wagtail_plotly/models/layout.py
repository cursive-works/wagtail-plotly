from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _


from wagtail.admin.edit_handlers import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
)

from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField

from ..widgets.palette import PaletteChooser


class LayoutTitle(models.Model):
    """
    Abstract layout title model
    """
    title_font_family = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('HTML font family - the typeface that will be applied by the web browser'),
    )
    title_font_size = models.PositiveSmallIntegerField(
        default=24,
        validators=[MinValueValidator(1), MaxValueValidator(144)],
        help_text=_('number greater than or equal to 1'),
    )
    title_font_color = ColorField(default='#444444')
    title_xref = models.CharField(
        max_length=10,
        default='container',
        choices=[
            ('container', _('Container')),
            ('paper', _('Paper')),
        ],
        help_text=_(
            (
                'Sets the container `x` refers to. "container" spans the entire '
                '`width` of the plot. "paper" refers to the width of the plotting area only.'
            )
        ),
    )
    title_yref = models.CharField(
        max_length=10,
        default='container',
        choices=[
            ('container', _('Container')),
            ('paper', _('Paper')),
        ],
        help_text=_(
            (
                'Sets the container `y` refers to. "container" spans the entire '
                '`height` of the plot. "paper" refers to the height of the plotting area only.'
            )
        ),
    )
    title_x = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_(
            'Sets the x position with respect to `xref` in normalized coordinates from "0" (left) to "1" (right).'
        ),
    )
    title_y = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_(
            'Sets the y position with respect to `yref` in normalized coordinates from "0" (bottom) to "1" (top). '
            'An empty value sets y position to "auto" (default) and places the baseline of the title onto the vertical '
            'center of the top margin.'
        ),
    )
    title_xanchor = models.CharField(
        max_length=10,
        default='auto',
        choices=[
            ('auto', _('Auto')),
            ('left', _('Left')),
            ('center', _('Center')),
            ('right', _('Right'))
        ],
        help_text=_(
            (
                'Sets the titles horizontal alignment with respect to its x position. '
                '"left" means that the title starts at x, "right" means that the title '
                'ends at x and "center" means that the titles center is at x. "auto" divides '
                '`xref` by three and calculates the `xanchor` value automatically based on the value of `x`.'
            )
        ),
    )
    title_yanchor = models.CharField(
        max_length=10,
        default='auto',
        choices=[
            ('auto', _('Auto')),
            ('top', _('Top')),
            ('middle', _('Middle')),
            ('bottom', _('Bottom')),
        ],
        help_text=_(
            (
                'Sets the titles vertical alignment with respect to its y position. '
                '"top" means that the titles cap line is at y, "bottom" means that the '
                'titles baseline is at y and "middle" means that the titles midline is at y. '
                '"auto" divides `yref` by three and calculates the `yanchor` value automatically '
                'based on the value of `y`.'
            )
        ),
    )
    title_pad_t = models.PositiveSmallIntegerField(
        default=0,
        help_text=_('The amount of padding (in px) along the top of the component'),
    )
    title_pad_r = models.PositiveSmallIntegerField(
        default=0,
        help_text=_('The amount of padding (in px) on the right side of the component'),
    )
    title_pad_b = models.PositiveSmallIntegerField(
        default=0,
        help_text=_('The amount of padding (in px) along the bottom of the component'),
    )
    title_pad_l = models.PositiveSmallIntegerField(
        default=0,
        help_text=_('The amount of padding (in px) on the left side of the component'),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title_font_family'),
                FieldPanel('title_font_size'),
                NativeColorPanel('title_font_color'),
                FieldPanel('title_xref'),
                FieldPanel('title_yref'),
                FieldPanel('title_x'),
                FieldPanel('title_y'),
                FieldPanel('title_xanchor'),
                FieldPanel('title_yanchor'),
                FieldPanel('title_pad_t'),
                FieldPanel('title_pad_r'),
                FieldPanel('title_pad_b'),
                FieldPanel('title_pad_l'),
            ],
            heading=_("Title"),
            classname="collapsible collapsed"
        ),
    ]

    class Meta:
        abstract = True


class LayoutFont(models.Model):
    """
    Abstract layout font model
    """
    font_family = models.CharField(
        max_length=255,
        blank=True,
        default='"Open Sans", verdana, arial, sans-serif',
        help_text=_('HTML font family - the typeface that will be applied by the web browser'),
    )
    font_size = models.PositiveSmallIntegerField(
        default=14,
        validators=[MinValueValidator(1), MaxValueValidator(72)]
    )
    font_color = ColorField(default='#444444')

    panels = [
        MultiFieldPanel(
            [
                HelpPanel(_(
                    (
                        'Sets the global font. Note that fonts used in traces and other layout components '
                        'inherit from the global font.'
                    )
                )),
                FieldPanel('font_family'),
                FieldPanel('font_size'),
                NativeColorPanel('font_color'),
            ],
            heading=_("Font"),
            classname="collapsible collapsed"
        ),
    ]

    class Meta:
        abstract = True


class LayoutLegend(models.Model):
    """
    Abstract layout legend model
    """
    showlegend = models.BooleanField(
        default=True,
        help_text=_(
            (
                'Determines whether or not a legend is drawn. Default is `TRUE` if there is a trace to show and '
                'any of these: a) Two or more traces would by default be shown in the legend. b) One pie trace is '
                'shown in the legend. c) One trace is explicitly given with `showlegend: TRUE`.'
            )
        ),
    )

    legend_bgcolor = ColorField(
        default='#FFFFFF',
        help_text=_('Sets the legend background color'),
    )
    legend_bordercolor = ColorField(
        default='#444444',
        help_text=_('Sets the color of the border enclosing the legend'),
    )
    legend_borderwidth = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
        ],
        help_text=_('Sets the width (in px) of the border enclosing the legend'),
    )
    legend_font_family = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('HTML font family - the typeface that will be applied by the web browser'),
    )
    legend_font_size = models.PositiveSmallIntegerField(
        default=14,
        validators=[MinValueValidator(1), MaxValueValidator(72)]
    )
    legend_font_color = ColorField(default='#444444')
    legend_orientation = models.CharField(
        max_length=1,
        default='v',
        choices=[
            ('v', _('Vertical')),
            ('h', _('Horizontal')),
        ],
        help_text=_('Sets the orientation of the legend'),
    )
    legend_traceorder = models.CharField(
        max_length=20,
        default='normal',
        choices=[
            ('normal', _('Normal')),
            ('reversed', _('Reversed')),
            ('grouped', _('Grouped')),
            ('reversed+grouped', _('Reversed Grouped'))
        ],
        help_text=_('Determines the order at which the legend items are displayed'),
    )
    legend_itemsizing = models.CharField(
        max_length=10,
        default='trace',
        choices=[
            ('trace', _('Trace')),
            ('constant', _('Constant')),
        ],
        help_text=_(
            (
                'Determines if the legend items symbols scale with their corresponding '
                '"trace" attributes or remain "constant" independent of the symbol size on the graph'
            )
        ),
    )
    legend_itemwidth = models.PositiveSmallIntegerField(
        default=30,
        validators=[
            MinValueValidator(30),
        ],
        help_text=_('Sets the width (in px) of the legend item symbols'),
    )
    legend_itemclick = models.CharField(
        blank=True,
        max_length=20,
        default='toggle',
        choices=[
            ('toggle', _('Toggle')),
            ('toggleothers', _('Toggle others')),
        ],
        help_text=_('Determines the behavior on legend item click'),
    )
    legend_itemdoubleclick = models.CharField(
        blank=True,
        max_length=20,
        default='toggleothers',
        choices=[
            ('toggle', _('Toggle')),
            ('toggleothers', _('Toggle others')),
        ],
        help_text=_('Determines the behavior on legend item double-click'),
    )
    legend_x = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(-2), MaxValueValidator(3)],
        help_text=_(
            (
                'Sets the x position (in normalized coordinates) of the legend. Defaults to "1.02" for vertical '
                'legends and defaults to "0" for horizontal legends.'
            )
        ),
    )
    legend_xanchor = models.CharField(
        max_length=10,
        default='left',
        choices=[
            ('auto', _('Auto')),
            ('left', _('Left')),
            ('center', _('Center')),
            ('right', _('Right'))
        ],
        help_text=_(
            (
                'Sets the titles horizontal alignment with respect to its x position. "left" means that the title '
                'starts at x, "right" means that the title ends at x and "center" means that the titles center '
                'is at x. "auto" divides `xref` by three and calculates the `xanchor` value automatically based '
                'on the value of `x`.'
            )
        ),
    )
    legend_y = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(-2), MaxValueValidator(3)],
        help_text=_(
            (
                'Sets the y position (in normalized coordinates) of the legend. Defaults to "1" for vertical '
                'legends, defaults to "-0.1" for horizontal legends.'
            )
        ),
    )
    legend_yanchor = models.CharField(
        max_length=10,
        default='auto',
        choices=[
            ('auto', _('Auto')),
            ('top', _('Top')),
            ('middle', _('Middle')),
            ('bottom', _('Bottom')),
        ],
        help_text=_(
            (
                'Sets the legends vertical position anchor This anchor binds the `y` position to the '
                '"top", "middle" or "bottom" of the legend. Value "auto" anchors legends at their bottom '
                'for `y` values less than or equal to 1/3, anchors legends to at their top for `y` values '
                'greater than or equal to 2/3 and anchors legends with respect to their middle otherwise.'
            )
        ),
    )
    legend_valign = models.CharField(
        max_length=10,
        default='middle',
        choices=[
            ('top', _('Top')),
            ('middle', _('Middle')),
            ('bottom', _('Bottom')),
        ],
        help_text=_('Sets the vertical alignment of the symbols with respect to their associated text'),
    )
    # Legend title
    legend_title_text = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Sets the title of the legend'),
    )
    legend_title_side = models.CharField(
        max_length=10,
        blank=True,
        choices=[
            ('top', _('Top')),
            ('left', _('Left')),
            ('top left', _('Top Left')),
        ],
        help_text=_(
            (
                'Determines the location of legends title with respect to the legend items. '
                'Defaulted to "top" with `orientation` is "h". Defaulted to "left" with `orientation` is "v". '
                'The "top left" options could be used to expand legend area in both x and y sides.'
            )
        ),
    )
    legend_title_font_family = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('HTML font family - the typeface that will be applied by the web browser'),
    )
    legend_title_font_size = models.PositiveSmallIntegerField(
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(72)]
    )
    legend_title_font_color = ColorField(default='#444444')

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('showlegend'),
                NativeColorPanel('legend_bgcolor'),
                NativeColorPanel('legend_bordercolor'),
                FieldPanel('legend_borderwidth'),

                FieldPanel('legend_font_family'),
                FieldPanel('legend_font_size'),
                NativeColorPanel('legend_font_color'),

                FieldPanel('legend_orientation'),
                FieldPanel('legend_traceorder'),

                FieldPanel('legend_itemsizing'),
                FieldPanel('legend_itemwidth'),
                FieldPanel('legend_itemclick'),
                FieldPanel('legend_itemdoubleclick'),

                FieldPanel('legend_x'),
                FieldPanel('legend_xanchor'),
                FieldPanel('legend_y'),
                FieldPanel('legend_yanchor'),
                FieldPanel('legend_valign'),

                FieldPanel('legend_title_text'),
                FieldPanel('legend_title_font_family'),
                FieldPanel('legend_title_font_size'),
                NativeColorPanel('legend_title_font_color'),
                FieldPanel('legend_title_side'),
            ],
            heading=_("Legend"),
            classname="collapsible collapsed"
        ),
    ]

    class Meta:
        abstract = True


class LayoutMargin(models.Model):
    """
    Abstract layout margin model
    """
    margin_l = models.PositiveSmallIntegerField(
        default=80,
        help_text=_('Sets the left margin (in px)'),
    )
    margin_r = models.PositiveSmallIntegerField(
        default=80,
        help_text=_('Sets the right margin (in px)'),
    )
    margin_t = models.PositiveSmallIntegerField(
        default=100,
        help_text=_('Sets the top margin (in px)'),
    )
    margin_b = models.PositiveSmallIntegerField(
        default=80,
        help_text=_('Sets the bottom margin (in px)'),
    )
    margin_pad = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text=_('Sets the amount of padding (in px) between the plotting area and the axis lines'),
    )
    margin_autoexpand = models.BooleanField(
        default=True,
        help_text=_(
            (
                'Turns on/off margin expansion computations. Legends, colorbars, updatemenus, sliders, '
                'axis rangeselector and rangeslider are allowed to push the margins by defaults.'
            )
        ),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('margin_l'),
                FieldPanel('margin_r'),
                FieldPanel('margin_t'),
                FieldPanel('margin_b'),
                FieldPanel('margin_pad'),
                FieldPanel('margin_autoexpand'),
            ],
            heading=_("Margin"),
            classname="collapsible collapsed"
        ),
    ]

    class Meta:
        abstract = True


class Layout(LayoutTitle, LayoutFont, LayoutLegend, LayoutMargin):

    title = models.CharField(
        max_length=255,
        help_text=_('Layout title for use in Wagtail (not used by Plotly)'),
    )

    autosize = models.BooleanField(
        default=True,
        help_text=_(
            (
                'Determines whether or not a layout width or height that has been left undefined by the user is '
                'initialized on each relayout. Note that, regardless of this attribute, an undefined layout width '
                'or height is always initialized on the first call to plot.'
            )
        ),
    )
    width = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(10),
        ],
        help_text=_('Sets the plots width (in px)'),
    )

    height = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(10),
        ],
        help_text=_('Sets the plots height (in px)'),
    )
    paper_bgcolor = ColorField(
        default='#FFFFFF',
        help_text=_('Sets the background color of the paper where the graph is drawn'),
    )
    plot_bgcolor = ColorField(
        default='#FFFFFF',
        help_text=_('Sets the background color of the plotting area in-between x and y axes'),
    )

    xaxis_gridcolor = ColorField(
        default='#EEEEEE',
        help_text=_('Sets the xaxis grid color'),
    )
    yaxis_gridcolor = ColorField(
        default='#EEEEEE',
        help_text=_('Sets the yaxis grid color'),
    )

    colorway = models.ForeignKey(
        'wagtail_plotly.Palette',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('title'),
                FieldPanel('autosize'),
                FieldPanel('width'),
                FieldPanel('height'),
                NativeColorPanel('paper_bgcolor'),
                NativeColorPanel('plot_bgcolor'),
                NativeColorPanel('xaxis_gridcolor'),
                NativeColorPanel('yaxis_gridcolor'),
                FieldPanel('colorway', widget=PaletteChooser),
            ],
            heading=_("General"),
            classname="collapsible"
        ),
    ] + LayoutTitle.panels + LayoutFont.panels + LayoutLegend.panels + LayoutMargin.panels

    def to_dict(self):
        """
        Convert the layout to a dictionary
        """
        data = model_to_dict(self, exclude=['id', 'title', 'colorway'])
        data = {k: v for k, v in data.items() if v != ''}

        # Remove None key
        if data.get('title_y', '') is None:
            del data['title_y']

        # Convert None to False
        data['legend_itemclick'] = data.get('legend_itemclick') or False
        data['legend_itemdoubleclick'] = data.get('legend_itemdoubleclick') or False

        # Convert colorway fk palette to list
        data['colorway'] = self.colorway.values() if self.colorway else self.colorway

        return data

    def __str__(self):
        return self.title
