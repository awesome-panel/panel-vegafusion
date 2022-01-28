import panel as pn
from panel.widgets.base import Widget
from .models import html_button_model
import param

class HTMLButton(Widget):
    # Set the Bokeh model to use
    _widget_type = html_button_model.HTMLButton

    # Rename Panel Parameters -> Bokeh Model properties
    # Parameters like title that does not exist on the Bokeh model should be renamed to None
    _rename = {
        "title": None,
    }

    # Parameters to be mapped to Bokeh model properties
    object = param.String(default=html_button_model.DEFAULT_OBJECT)
    clicks = param.Integer(default=0)