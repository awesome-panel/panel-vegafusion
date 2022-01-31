"""The panel-vegafusion renderer for Altair"""
# pylint: skip-file
# Source: https://github.com/vegafusion/vegafusion/blob/main/python/vegafusion-jupyter/vegafusion_jupyter/transformer.py

# VegaFusion
# Copyright (C) 2022, Jon Mease
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import altair as alt

NAME = "panel-vegafusion"

def vegafusion_renderer(spec, **widget_options):
    """
    Altair renderer that displays charts using the Panel VegaFusion pane
    """
    from IPython.display import display
    from panel_vegafusion import VegaFusion

    # Display widget as a side effect, then return empty string text representation
    # so that Altair doesn't also display a string representation
    
    # Not tested yet. Don't know if it will work
    widget = VegaFusion(spec, **widget_options)
    display(widget)
    return {'text/plain': ""}

def register():
    """Register the 'panel-vegafusion' renderer for Altair"""
    alt.renderers.register(NAME, vegafusion_renderer)