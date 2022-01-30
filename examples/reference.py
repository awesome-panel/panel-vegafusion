import altair as alt
import panel as pn
from panel_vegafusion import VegaFusion
from panel_vegafusion.utils import get_plot, ALTAIR_BLUE, get_theme


pn.extension(template="fast")

theme=get_theme()
alt.themes.enable(theme)

plot=get_plot() # Can be replaced any Altair plot or Vega Specification

component = VegaFusion(plot, height=800).servable()

pn.state.template.param.update(
    site="Panel VegaFusion", title="Interactive BIG DATA apps with CROSSFILTERING using Altair or Vega",
    accent_base_color=ALTAIR_BLUE, header_background=ALTAIR_BLUE,
)