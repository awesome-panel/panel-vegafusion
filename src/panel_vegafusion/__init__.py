import json
import logging
from typing import Optional, Union

import altair as alt
import param
from panel.reactive import ReactiveHTML

from ._utils import edit_constant, get_chart

logger = logging.getLogger("panel-vegafusion")

import vegafusion_jupyter as vf

vf.enable()


class VegaFusion(ReactiveHTML):
    """A Panel pane for Altair charts and Vega dictionaries rendered by VegaFusion"""

    # object = param.ClassSelector(class_=(alt.TopLevelMixin, dict), allow_None=True, doc="""
    #     An altair chart or vega-lite dictionary""")

    verbose = param.Boolean(default=False, doc="""Whether to log or not""")
    indent = param.Integer(2, doc="""The indentation of json specifications""")

    debounce_wait = param.Number(30, allow_None=False)
    debounce_max_wait = param.Number(60, allow_None=True)

    spec = param.String(
        doc="""The Vega json specification derived from the object""",
        allow_None=True,
        readonly=True,
    )
    full_vega_spec = param.String(None, allow_None=True, readonly=True)
    client_vega_spec = param.String(None, allow_None=True, readonly=True)
    server_vega_spec = param.String(None, allow_None=True, readonly=True)
    comm_plan = param.String(None, allow_None=True, readonly=True)

    download_source_link = param.String(None, allow_None=True)

    _template = """
<div id="view" style="height:100%;width:100%">Hello</div>    
"""

    _request = param.String()
    _response = param.String()

    def __init__(self, object: Optional[Union[alt.TopLevelMixin, dict]] = None, **params):
        self.object = object
        super().__init__(**params)
        self._update_spec()

    def _update_spec(self):
        object = self.object
        if isinstance(object, alt.TopLevelMixin):
            if alt.data_transformers.active == "vegafusion-feather":
                data_transformer_opts = alt.data_transformers.options
            else:
                data_transformer_opts = dict()

            with alt.renderers.enable("vegafusion"):
                with alt.data_transformers.enable("vegafusion-feather", **data_transformer_opts):
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


if __name__.startswith("bokeh"):
    VegaFusion(object=get_chart()).servable()
