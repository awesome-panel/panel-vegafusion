"""Tests of the vegafusion_pane module"""
import altair as alt
import pandas as pd
import pytest

from panel_vegafusion import VegaFusion

# pylint: disable=redefined-outer-name


@pytest.fixture
def chart():
    """Returns an Altair Chart"""
    source = pd.DataFrame(
        {
            "a": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            "b": [28, 55, 43, 91, 81, 53, 19, 87, 52],
        }
    )

    return alt.Chart(source).mark_bar().encode(x="a", y="b")


@pytest.fixture
def spec(chart) -> dict:
    """Returns the vega spec of the chart"""
    return chart.to_dict()


def test_constructor_altair(chart):
    """We can construct from Altair"""
    component = VegaFusion(object=chart)
    assert component.spec


def test_constructor_dict(spec):
    """We can construct from Vega spec"""
    component = VegaFusion(object=spec)
    assert component.spec


def test_constructor_none():
    """We can construct from None"""
    component = VegaFusion()
    assert not component.spec
