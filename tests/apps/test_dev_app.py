import panel as pn
from panel_vegafusion.utils import get_plot, ALTAIR_BLUE
from panel_vegafusion import VegaFusion

pn.extension("ace", template="fast")

accent = ALTAIR_BLUE

VegaFusion.enable()
chart = get_plot()()

component = VegaFusion(chart, verbose=False, height=800).servable(area="main")
settings = pn.Param(component, parameters=["verbose", "debounce_wait", "debounce_max_wait"], name="VegaFusion Settings").servable(area="sidebar")
pn.Accordion(
    component.param.spec,
    component.param.full_vega_spec,
    component.param.client_vega_spec,
    component.param.server_vega_spec,
    component.param.comm_plan,
    component.param.download_source_link,
).servable(area="sidebar")

pn.state.template.param.update(
    site="Panel meets VegaFusion", title="Interactive BIG DATA apps with CROSSFILTERING for Altair and Vega - PROOF OF CONCEPT",
    accent_base_color=accent, header_background=accent,
)
