import json
import logging
import time
import altair as alt
import param

from ._utils import edit_constant
import panel as pn
from panel.reactive import ReactiveHTML

logger = logging.getLogger("panel-vegafusion")
from vegafusion_jupyter.runtime import runtime

VEGA_FUSION_CSS = """
.vegafusion-loading {
  color: red;
  background: aqua;
}
.vegafusion-loading .inner {
  width: 100px;
}
.vegafusion-embed {
  min-height: 40px;
  position: relative;
  display: inline-block;
  box-sizing: border-box;
  overflow: visible;
}
.vegafusion-embed.has-actions {
  padding-right: 38px;
}
.vegafusion-embed details:not([open]) > :not(summary) {
  display: none !important;
}
.vegafusion-embed summary {
  list-style: none;
  position: absolute;
  top: 0;
  right: 0;
  padding: 6px;
  z-index: 1000;
  background: white;
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
  color: #1b1e23;
  border: 1px solid #aaa;
  border-radius: 999px;
  opacity: 0.2;
  transition: opacity 0.4s ease-in;
  outline: none;
  cursor: pointer;
  line-height: 0px;
}
.vegafusion-embed summary::-webkit-details-marker {
  display: none;
}
.vegafusion-embed summary:active {
  box-shadow: #aaa 0px 0px 0px 1px inset;
}
.vegafusion-embed summary svg {
  width: 16px;
  height: 16px;
}
.vegafusion-embed details[open] summary {
  opacity: 0.5;
}
.vegafusion-embed:hover summary, .vegafusion-embed:focus summary {
  opacity: 0.7 !important;
  transition: opacity 0.2s ease;
}
.vegafusion-embed .vegafusion-actions {
  position: absolute;
  z-index: 1001;
  top: 35px;
  right: -9px;
  display: flex;
  flex-direction: column;
  padding-bottom: 8px;
  padding-top: 8px;
  border-radius: 4px;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.2);
  border: 1px solid #d9d9d9;
  background: white;
  animation-duration: 0.15s;
  animation-name: scale-in;
  animation-timing-function: cubic-bezier(0.2, 0, 0.13, 1.5);
  text-align: left;
}
.vegafusion-embed .vegafusion-actions hr {
  width: auto;
  height: 1px;
  border: none;
  background-color: #434a56;
  margin: 4px 10px 4px 10px;
  opacity: 50%;
}
.vegafusion-embed .vegafusion-actions .source-msg {
  padding: 4px 16px;
  font-family: sans-serif;
  font-size: 10px;
  font-weight: 400;
  max-width: 180px;
  color: #CD5C5C;
}
.vegafusion-embed .vegafusion-actions a {
  padding: 4px 16px;
  font-family: sans-serif;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  color: #434a56;
  text-decoration: none;
}
.vegafusion-embed .vegafusion-actions a:hover {
  background-color: #f7f7f9;
  color: black;
}
.vegafusion-embed .vegafusion-actions::before, .vegafusion-embed .vegafusion-actions::after {
  content: "";
  display: inline-block;
  position: absolute;
  pointer-events: none;
}
.vegafusion-embed .vegafusion-actions::before {
  left: auto;
  right: 14px;
  top: -16px;
  border: 8px solid #0000;
  border-bottom-color: #d9d9d9;
}
.vegafusion-embed .vegafusion-actions::after {
  left: auto;
  right: 15px;
  top: -14px;
  border: 7px solid #0000;
  border-bottom-color: #fff;
}
.vegafusion-embed .chart-wrapper.fit-x {
  width: 100%;
}
.vegafusion-embed .chart-wrapper.fit-y {
  height: 100%;
}

.vegafusion-embed-wrapper {
  max-width: 100%;
  overflow: auto;
  padding-right: 14px;
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.6);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
"""

# Jupyter Python Widget: https://github.com/vegafusion/vegafusion/blob/main/python/vegafusion-jupyter/vegafusion_jupyter/widget.py
# IPywidget Client Widget: https://github.com/vegafusion/vegafusion/blob/main/python/vegafusion-jupyter/src/widget.ts

class VegaFusion(ReactiveHTML):
    object = param.ClassSelector(class_=(alt.TopLevelMixin, dict), allow_None=True, doc="""
        An altair chart or vega-lite dictionary""")
    spec = param.String(
        doc="""The Vega json specification derived from the object""",
        allow_None=True,
        readonly=True,
    )
    scale_factor = param.Number(1.0, bounds=(0,None))
    verbose = param.Boolean(default=False, doc="""Whether to log or not""")
    indent = param.Integer(2, doc="""The indentation of json specifications""")
    debounce_wait = param.Number(30, allow_None=False)
    debounce_max_wait = param.Number(60, allow_None=True)
    full_vega_spec = param.String(None, allow_None=True, readonly=True)
    client_vega_spec = param.String(None, allow_None=True, readonly=True)
    server_vega_spec = param.String(None, allow_None=True, readonly=True)
    comm_plan = param.String(None, allow_None=True, readonly=True)
    download_source_link = param.String(None, allow_None=True)
    _request = param.List()
    _response = param.List()

    _template = """
<div id="containerElement" class="chart-wrapper" style="height:100%;width:100%;">
    <div id="viewElement" style="height:100%;width:100%;">Loading ...</div>
</div>
<div id="menuElement">
    <details id="detailElement" title="Click to view actions" onClick="${script('closeDetailElement')}">
        <summary>
            <svg id="svgElement" version="1.1" viewBox="0.0 0.0 946.4776902887139 673.4829396325459" fill="none" stroke="none" stroke-linecap="square" stroke-miterlimit="10" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg"><clipPath id="p.0"><path d="m0 0l946.47766 0l0 673.4829l-946.47766 0l0 -673.4829z" clip-rule="nonzero"></path></clipPath><g clip-path="url(#p.0)"><path fill="#000000" fill-opacity="0.0" d="m0 0l946.47766 0l0 673.4829l-946.47766 0z" fill-rule="evenodd"></path><path fill="#434a56" d="m241.20998 355.4672l228.50392 0l0 318.04727l-228.50392 0z" fill-rule="evenodd"></path><path fill="#434a56" d="m601.9989 0l-65.49762 177.0l343.29565 0.9973755l65.87903 -177.99738z" fill-rule="evenodd"></path><path fill="#434a56" d="m505.0006 317.5013l-42.4993 177.0l302.89688 0.15222168l64.59503 -177.88187z" fill-rule="evenodd"></path><path fill="#434a56" d="m0.46194226 -0.04330709l240.56693 673.5696l127.509186 -285.16272l-140.021 -388.40683z" fill-rule="evenodd"></path><path fill="#434a56" d="m712.8845 -0.01968504l-242.1799 673.54333l-229.69412 0l242.1799 -673.54333z" fill-rule="evenodd"></path></g></svg>
        </summary>
        <div class="vegafusion-actions">
            <a id="saveToSVG" href="#" target="_blank" download="visualization.svg" title="" onMouseDown="${script('exportToSVG')}">Save as SVG</a>
            <a id="saveToPNG" href="#" target="_blank" download="visualization.png" title="" onMouseDown="${script('exportToPNG')}">Save as PNG</a>
            <hr/>
            <a href="https://github.com/vegafusion/vegafusion" target="_blank" title="">About VegaFusion</a>
            <a href="https://www.gnu.org/licenses/agpl-3.0.en.html" target="_blank" title="https://www.gnu.org/licenses/agpl-3.0.en.html">AGPLv3 License</a>
            <p class="source-msg" title="">VegaFusion's AGPLv3 license requires the author to provide this application's source code upon request.</p>
            <hr/>
            <a href="https://panel.holoviz.org/" target="_blank" title="">About Panel</a>
            <a href="https://github.com/MarcSkovMadsen/panel-vegafusion" target="_blank" title="">About Panel VegaFusion</a>
            <a href="https://awesome-panel.org/" target="_blank" title="">About Awesome Panel</a>
        </div>
    </details>
</div>
"""

    __javascript_modules__ = [
        "dist/main.js"
    ]
    
    _scripts = {
        "render": """
console.log("render - start", new Date())
state.viewElement=viewElement
state.detailElement=detailElement
view.el.classList.add("vegafusion-embed");
view.el.classList.add("has-actions");

function render_core(panelVegaFusion){
    state.render_vegafusion=panelVegaFusion.render_vegafusion
    state.vegalite_compile = panelVegaFusion.compile
    state.vegafusion_handle = null
    console.log("panelVegaFusion imported", new Date())
    self.value_changed()    
}

window.getPanelVegaFusion().then(object=>render_core(object))
console.log("render - start", new Date())
""", 
    "after_layout": """setTimeout(function(){window.dispatchEvent(new Event('resize'))}, 25);""",
    "value_changed": """
console.log("value_changed - start", self)

spec = data.spec;
if (spec !== null) {
    let parsed = JSON.parse(spec);
    let vega_spec_json;
    if (parsed["$schema"].endsWith("schema/vega/v5.json")) {
        vega_spec_json = spec
    } else {
        // Assume we have a Vega-Lite spec, compile to vega
        console.log("vegalist_compile", state.vegalite_compile)
        let vega_spec = state.vegalite_compile(parsed);
        vega_spec_json = JSON.stringify(vega_spec.spec);
    }

    state.vegafusion_handle = state.render_vegafusion(
        state.viewElement,
        vega_spec_json,
        data.verbose || false,
        data.debounce_wait || 30,
        data.debounce_max_wait,
        (request) => {
            if (data.verbose) {
                console.log("VegaFusion sent request: ", request)
            }
            data._request=request
        });

    // Update vega spec properties
    if (data.verbose){
        data.full_vega_spec=vega_spec_json;
        data.client_vega_spec=state.vegafusion_handle.client_spec_json();
        data.server_vega_spec=state.vegafusion_handle.server_spec_json();
        data.comm_plan=state.vegafusion_handle.comm_plan_json();
    } else {
        data.full_vega_spec="Set verbose=True to get this";
        data.client_vega_spec="Set verbose=True to get this";
        data.server_vega_spec="Set verbose=True to get this";
        data.comm_plan="Set verbose=True to get this";
    }
    
    console.log("panelVegaFusion component updated", new Date())
}

console.log("value_changed - end")
""", 
    "spec": "self.value_changed()",
    "verbose": "self.value_changed()",
    "debounce_wait": "self.value_changed()",
    "debounce_max_wait": "self.value_changed()",
    "download_source_link": "self.value_changed()",
    "_response": """
bytes = data._response
if (data.verbose) {
    console.log("VegaFusion received response: ", bytes)
}
state.vegafusion_handle.receive(bytes)
""",
    "exportToSVG": """
event.preventDefault();
if (state.vegafusion_handle) {
  state.vegafusion_handle.to_image_url("svg", data.scale_factor).then(object=>event.target.href=object);
  
}   
""",
    "exportToPNG": """
event.preventDefault();
if (state.vegafusion_handle) {
  state.vegafusion_handle.to_image_url("png", data.scale_factor).then(object=>event.target.href=object);
}   
""",
    "closeDetailElement": """
if (event.target===svgElement && state.detailElement.open){
  event.preventDefault()
  state.detailElement.removeAttribute('open');
} else if (state.detailElement.contains(event.target) && state.detailElement.open) {
  state.detailElement.removeAttribute('open');
}"""
          
    }

    def __init__(self, object, **params):
        super().__init__(object=object, **params)

    _rename = {"object": None}

    @param.depends("object", watch=True, on_init=True)
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
            # logger.level = logging.INFO
            # logging.info(msg)
            print(msg)

    @staticmethod
    def enable():
        import vegafusion_jupyter as vf

        vf.enable()

        if not VEGA_FUSION_CSS in pn.config.raw_css:
            pn.config.raw_css.append(VEGA_FUSION_CSS)


    @param.depends("_request", watch=True)
    def _handle_request(self):
        start = time.time()
        self._log(f"VegaFusion received request: {self._request}"[0:100] + "...")
        request_bytes = bytes(self._request)
        self._log(f"VegaFusion received request_bytes: {request_bytes}"[0:100] + "...")

        # Build response
        response_bytes = runtime.process_request_bytes(request_bytes)
        self._response = list(response_bytes)

        duration = (time.time() - start) * 1000
        self._log(f"VegaFusion sent response_bytes in {duration:.1f}ms: {response_bytes}"[0:100] + "...")
        self._log(f"VegaFusion sent response in {duration:.1f}ms: {self._response}"[0:100] + "...")