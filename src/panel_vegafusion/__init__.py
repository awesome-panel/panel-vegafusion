"""
The [Panel VegaFusion pane](https://github.com/marcskovmadsen/panel-vegafusion) allows you to create interactive big data apps based on 
the [Altair](https://altair-viz.github.io/index.html) plotting library and the 
[Vega](https://vega.github.io/vega/) visualization specification.

It is all powered by [VegaFusion](https://github.com/vegafusion/vegafusion) which provides 
serverside acceleration for the Vega visualization grammar.

## Example

```python
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
    site="Panel VegaFusion", title="Interactive BIG DATA apps with CROSSFILTERING for Altair and Vega",
    accent_base_color=ALTAIR_BLUE, header_background=ALTAIR_BLUE,
)
```

[![Follow on Twitter](https://img.shields.io/twitter/follow/MarcSkovMadsen.svg?style=social)](https://twitter.com/MarcSkovMadsen)
"""

from .vegafusion_pane import VegaFusion
