"""Tests of the utils module"""
import pytest

from panel_vegafusion.utils import bundle

# pylint: disable=redefined-outer-name


@pytest.fixture
def target(tmp_path):
    """Returns the target path fixture"""
    return tmp_path / "dist" / "bundled" / "panel-vegafusion"


def test_bundle(target):
    """Test that we can bundle asset, i.e. copy them into the Panel assets bundle subfolder"""
    bundle(target=target)
    assert (target / "main.js").is_file()


def test_bundle_multiple(target):
    """Test that we can bundle asset multiple times"""
    bundle(target=target)
    bundle(target=target)
