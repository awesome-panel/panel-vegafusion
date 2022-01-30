![Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MarcSkovMadsen/panel-vegafusion/HEAD?urlpath=lab) [![Follow on Twitter](https://img.shields.io/twitter/follow/MarcSkovMadsen.svg?style=social)](https://twitter.com/MarcSkovMadsen)

# Panel VegaFusion

PROOF OF CONCEPT CURRENTLY

The [Panel VegaFusion pane](https://github.com/marcskovmadsen/panel-vegafusion) allows you to
create interactive big data apps based on the [Altair](https://altair-viz.github.io/index.html)
plotting library and the [Vega](https://vega.github.io/vega/) visualization specification.

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
    site="Panel meets VegaFusion", title="Interactive BIG DATA apps with CROSSFILTERING for Altair and Vega",
    accent_base_color=ALTAIR_BLUE, header_background=ALTAIR_BLUE,
)
```

## License - AGPLv3 - IMPORTANT

This Panel Vegafusion project is AGPLv3 Licensed because VegaFusion is AGPLv3 licensed and *requires the
author to provide this application's source code upon request*.

I don't yet understand the implications for using it in a "real" product.

SO PLEASE INVESTIGATE THE LEGAL ASPECTS ON YOUR OWN. YOU WILL BE USING THIS REPO AT YOUR OWN
RISK ANYWAYS!

## Install

```bash
git clone https://github.com/MarcSkovMadsen/panel-vegafusion.git
conda create -n panel_vegafusion -c conda-forge python=3.9 nodejs
conda activate panel_vegafusion
pip install -e .[all]
```

## Develop

For now you can serve an example with hot reload via

```bash
panel serve 'examples/reference.py' --autoreload --show --static dist=./src-js/dist
```

If working on the `.ts` code you might want to add autorebuild via

```bash
watchmedo shell-command --patterns="*.ts" --recursive --command='echo "${watch_src_path}" & panel build src/panel_vegafusion & echo "Update" >> src/panel_vegafusion/update.py' src/panel_vegafusion/models
```

You will have to do a [hard refresh](https://fabricdigital.co.nz/blog/how-to-hard-refresh-your-browser-and-clear-cache) of your browser to load the newly build `.js` files.

You can find inspiration in the original Jupyter VegaFusion reference example via

```bash
jupyter lab tests/reference_example.ipynb
```

## Build

Bokeh Extension

```bash
panel build src/panel_vegafusion
```

panelVegaFusion js

```bash
cd src-js
npm run build
cd ..
```

## Test

```bash
pytest tests
```

## CodeSandbox - panelVegaFusion

[https://codesandbox.io/s/sleepy-carlos-2dqdt?file=/index.js](https://codesandbox.io/s/sleepy-carlos-2dqdt?file=/index.js)

## References

- [VegaFusion](https://github.com/vegafusion/vegafusion)
- [Feature Request for Panel Support](https://github.com/vegafusion/vegafusion/issues/62)

## Issues Identified

- https://github.com/holoviz/panel/issues/3149
- https://github.com/holoviz/param/issues/597
- [Bokeh Discourse - Cannot bokeh build extension with wasm dependency](https://discourse.bokeh.org/t/how-do-i-build-bokeh-extension-with-wasm-depencency/8842)
- [vegafusion/vegafusion #64 - Altair Dark theme not working](https://github.com/vegafusion/vegafusion/issues/64)
