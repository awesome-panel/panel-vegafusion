"""Utilities for working with Panel, VegaFusion and Altair"""
import shutil
from contextlib import contextmanager
from typing import Optional, Union

import panel as pn
import param
from importlib_metadata import pathlib

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
    for parameter in params:
        parameter.constant = False
        parameter.readonly = False
    try:
        yield
    except:  # pylint: disable=try-except-raise
        raise
    finally:
        for (parameter, const, readonly) in zip(params, constants, readonlys):
            parameter.constant = const
            parameter.readonly = readonly


def get_theme():
    """Returns the relevant theme ('default' or 'dark') based on url parameters"""
    return pn.state.session_args.get("theme", [b"default"])[0].decode()


BUNDLE_SOURCE_PATH = pathlib.Path(__file__).parent / "assets" / "bundled" / "panel-vegafusion"
BUNDLE_TARGET_PATH = pathlib.Path(pn.__file__).parent / "dist" / "bundled" / "panel-vegafusion"
BUNDLE_PANEL_URL_PREFIX = "static/extensions/panel/bundled/panel-vegafusion/"


def bundle(
    source: pathlib.Path = BUNDLE_SOURCE_PATH,
    target: pathlib.Path = BUNDLE_TARGET_PATH,
):
    """Copies the panel-vegafusion bundled assets to the Panel bundled assets folder

    Then they are are served by the server and available to the VegaFusion pane
    """
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(source), str(target), dirs_exist_ok=True)


def get_plot(
    theme: Optional[str] = None,
    height: Union[int, str] = "container",
    width: Union[int, str] = "container",
):
    """Returns an Altair Plot for demo and testing purposes"""
    # pylint: disable=import-outside-toplevel
    import altair as alt
    from vega_datasets import data

    # pylint: enable=import-outside-toplevel

    if not theme:
        theme = get_theme()
    if theme == "dark":
        alt.themes.enable("dark")
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
