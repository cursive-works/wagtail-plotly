import json

from django.forms import widgets


class JSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            return json.dumps(json.loads(value), indent=4)
        except Exception:
            return super().format_value(value)