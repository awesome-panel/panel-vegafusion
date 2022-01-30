import altair as alt
import pandas as pd
import pytest

from panel_vegafusion import VegaFusion


@pytest.fixture
def chart():
    source = pd.DataFrame(
        {
            "a": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            "b": [28, 55, 43, 91, 81, 53, 19, 87, 52],
        }
    )

    return alt.Chart(source).mark_bar().encode(x="a", y="b")


@pytest.fixture(scope="session", autouse=True)
def enable_vegafusion():
    VegaFusion.enable()


@pytest.fixture
def spec(chart):
    return chart.to_dict()


def test_constructor_altair(chart):
    component = VegaFusion(object=chart)
    assert component.spec


def test_constructor_dict(spec):
    component = VegaFusion(object=spec)
    assert component.spec


def test_constructor_none():
    component = VegaFusion()
    assert not component.spec
