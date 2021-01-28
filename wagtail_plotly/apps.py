from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailPlotlyAppConfig(AppConfig):
    name = 'wagtail_plotly'
    label = 'wagtail_plotly'
    verbose_name = _("Wagtail Plotly")
