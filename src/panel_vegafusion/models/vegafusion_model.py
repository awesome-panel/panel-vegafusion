# pylint: skip-file
"""This file is not used or finished. We keep it until we decide the current ReactiveHTML 
implementation is good enough."""
from bokeh.core.properties import Bool, Float, Int, Nullable, String
from bokeh.models import HTMLBox


class VegaFusion(HTMLBox):
    """Example implementation of a Custom Bokeh Model"""

    spec = String()
    verbose = Bool(default=False)
    indent = Int(default=2)
    debounce_wait = Float(default=30)
    debounce_max_wait = Nullable(Float(default=60))
    download_source_link = Nullable(String(default=None))
    full_vega_spec = Nullable(String(default=None))
    client_vega_spec = Nullable(String(default=None))
    server_vega_spec = Nullable(String(default=None))
    comm_plan = Nullable(String(default=None))
    _request = String(default="")
    _response = String(default="")
