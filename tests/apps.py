import panel as pn
from panel_vegafusion._utils import get_chart, ALTAIR_PALETTE
from panel_vegafusion.vega_fusion_pane_reactive import VegaFusion

pn.extension("ace", template="fast")

accent = ALTAIR_PALETTE[0]

VegaFusion.enable()
chart = get_chart()

# verbose
# indent
# debounce_wait
# debounce_max_wait
# full_vega_spec
# client_vega_spec
# server_vega_spec
# comm_plan
# download_source_link

component = VegaFusion(chart, verbose=True, height=800).servable(area="main")
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
    site="Panel meets VegaFusion", title="Interactive BIG DATA apps with easy CROSSFILTERING for Altair and Vega - PROOF OF CONCEPT",
    accent_base_color=accent, header_background=accent,
)
