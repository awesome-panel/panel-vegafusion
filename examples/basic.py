import panel as pn
import altair as alt
from vega_datasets import data

import vegafusion_jupyter as vf
vf.enable()

pn.extension("ipywidgets", template="fast")

ACCENT = "#1f77b4"
PALETTE = [ACCENT, "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

if not "panel-vegafusion" in pn.state.cache:
    seattle_weather = pn.state.cache["panel-vegafusion"]=data.seattle_weather()
else:
    seattle_weather = pn.state.cache["panel-vegafusion"]

def get_chart(seattle_weather):
    brush = alt.selection(type='interval', encodings=['x'])

    bars = alt.Chart().mark_bar().encode(
        x='month(date):O',
        y='mean(precipitation):Q',
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
    ).add_selection(
        brush
    )

    line = alt.Chart().mark_rule(color='firebrick').encode(
        y='mean(precipitation):Q',
        size=alt.SizeValue(3)
    ).transform_filter(
        brush
    )

    return alt.layer(bars, line, data=seattle_weather)

chart = get_chart(seattle_weather)

pn.panel(chart).servable()

pn.state.template.param.update(
    site="Vegafusion", title="Interactive Big Data Apps with Crossfiltering",
    accent_base_color=ACCENT, header_background=ACCENT
)