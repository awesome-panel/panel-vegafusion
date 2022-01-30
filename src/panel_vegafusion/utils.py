from contextlib import contextmanager
from typing import Optional

import panel as pn
import param

ALTAIR_BLUE = "#1f77b4"
ALTAIR_PALETTE = [
    ALTAIR_BLUE,
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


# Needed because of https://github.com/holoviz/param/issues/597
@contextmanager
def edit_constant(parameterized: param.Parameterized):
    """
    Temporarily set parameters on Parameterized object to constant=False
    to allow editing them.
    """
    params = parameterized.param.objects("existing").values()
    constants = [p.constant for p in params]
    readonlys = [p.readonly for p in params]
    for p in params:
        p.constant = False
        p.readonly = False
    try:
        yield
    except:
        raise
    finally:
        for (p, const, readonly) in zip(params, constants, readonlys):
            p.constant = const
            p.readonly = readonly


def get_theme():
    return pn.state.session_args.get("theme", [b"default"])[0].decode()


def get_plot(theme: Optional[str] = None, height="container", width="container"):
    import altair as alt
    from vega_datasets import data

    if not theme:
        theme = get_theme()
    if theme == "dark":
        alt.themes.enable("dark")
        print(theme)
    else:
        alt.themes.enable("default")

    key = "panel-vegafusion-chart"
    if key in pn.state.cache:
        seattle_weather = pn.state.cache[key]
    else:
        seattle_weather = pn.state.cache[key] = data.seattle_weather()

    brush = alt.selection(type="interval", encodings=["x"])

    bars = (
        alt.Chart()
        .mark_bar()
        .encode(
            x="month(date):O",
            y="mean(precipitation):Q",
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        )
        .add_selection(brush)
    )

    line = (
        alt.Chart()
        .mark_rule(color="firebrick")
        .encode(y="mean(precipitation):Q", size=alt.SizeValue(3))
        .transform_filter(brush)
    )

    return alt.layer(bars, line, data=seattle_weather).properties(
        height=height,
        width=width,
    )
