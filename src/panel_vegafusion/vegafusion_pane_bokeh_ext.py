import json
import logging

import altair as alt
import param
from panel.widgets.base import Widget

from .models import vegafusion_model
from .utils import edit_constant

logger = logging.getLogger("panel-vegafusion")

# Jupyter Python Widget: https://github.com/vegafusion/vegafusion/blob/main/python/vegafusion-jupyter/vegafusion_jupyter/widget.py
# IPywidget Client Widget: https://github.com/vegafusion/vegafusion/blob/main/python/vegafusion-jupyter/src/widget.ts


class VegaFusion(Widget):
    object = param.ClassSelector(
        class_=(alt.TopLevelMixin, dict),
        allow_None=True,
        doc="""
        An altair chart or vega-lite dictionary""",
    )
    spec = param.String(
        doc="""The Vega json specification derived from the object""",
        allow_None=True,
        readonly=True,
    )
    verbose = param.Boolean(default=False, doc="""Whether to log or not""")
    indent = param.Integer(2, doc="""The indentation of json specifications""")
    debounce_wait = param.Number(30, allow_None=False)
    debounce_max_wait = param.Number(60, allow_None=True)
    full_vega_spec = param.String(None, allow_None=True, readonly=True)
    client_vega_spec = param.String(None, allow_None=True, readonly=True)
    server_vega_spec = param.String(None, allow_None=True, readonly=True)
    comm_plan = param.String(None, allow_None=True, readonly=True)
    download_source_link = param.String(None, allow_None=True)
    _request = param.String()
    _response = param.String()

    # Set the Bokeh model to use
    _widget_type = vegafusion_model.VegaFusion

    # Rename to bokeh model properties or skip
    _rename = {
        "title": None,
        "object": None,
    }

    @param.depends("object", watch=True, on_init=True)
    def _update_spec(self):
        object = self.object
        if isinstance(object, alt.TopLevelMixin):
            if alt.data_transformers.active == "vegafusion-feather":
                data_transformer_opts = alt.data_transformers.options
            else:
                data_transformer_opts = dict()

            with alt.renderers.enable("vegafusion"):
                with alt.data_transformers.enable(
                    "vegafusion-feather", **data_transformer_opts
                ):
                    # Temporarily enable the vegafusion renderer and transformer so
                    # that we use them even if they are not enabled globally
                    _spec = object.to_dict()
        else:
            _spec = object

        with edit_constant(self):
            if isinstance(_spec, dict):
                self.spec = json.dumps(_spec, indent=self.indent)
            else:
                self.spec = None

        if alt.renderers.active == "vegafusion":
            # Use configured debounce options, if any
            renderer_opts = alt.renderers.options
            if "debounce_wait" in renderer_opts:
                self.debounce_wait = renderer_opts["debounce_wait"]

            if "debounce_max_wait" in renderer_opts:
                self.debounce_max_wait = renderer_opts["debounce_max_wait"]

    def _log(self, msg):
        if self.verbose:
            logger.info("panel.VegaFusion: %", msg)

    @staticmethod
    def enable():
        import vegafusion_jupyter as vf

        vf.enable()
