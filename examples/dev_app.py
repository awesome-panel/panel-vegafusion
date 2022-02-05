import panel as pn

from panel_vegafusion import VegaFusion
from panel_vegafusion.utils import ALTAIR_BLUE, get_plot


def test_dev_app():
    pn.extension(template="fast")

    accent = ALTAIR_BLUE

    chart = get_plot()

    component = VegaFusion(chart, verbose=True, height=800).servable(area="main")
    pn.Param(
        component,
        parameters=["verbose", "debounce_wait", "debounce_max_wait"],
        name="VegaFusion Settings",
    ).servable(area="sidebar")
    pn.Accordion(
        component.param.spec,
        component.param.full_vega_spec,
        component.param.client_vega_spec,
        component.param.server_vega_spec,
        component.param.comm_plan,
        component.param.download_source_link,
    ).servable(area="sidebar")

    pn.state.template.param.update(
        site="Panel VegaFusion",
        title="Interactive BIG DATA apps with CROSSFILTERING for Altair and Vega",
        accent_base_color=accent,
        header_background=accent,
    )


if __name__.startswith("bokeh"):
    test_dev_app()
