![Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Follow on Twitter](https://img.shields.io/twitter/follow/MarcSkovMadsen.svg?style=social)](https://twitter.com/MarcSkovMadsen)

# panel-vegafusion

WORK IN PROGRESS. NOT WORKING

Provides a [VegaFusion](https://github.com/vegafusion/vegafusion) component (pane) for Panel to enable interactive big data apps using Vega or Altair.

Check out the repository on Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MarcSkovMadsen/panel-vegafusion/HEAD?urlpath=lab)

## License - IMPORTANT

This reposity is MIT licensed. BUT the original VegaFusion is AGPLv3 licensed and *requires the
author to provide this application's source code upon request*.

I honestly believe there is no issue in creating a repository like this and exploring. But I
don't yet understand the implications for using in a "real" product.

SO PLEASE INVESTIGATE THE LEGAL ASPECTS ON YOUR OWN. YOU WILL BE USING THIS REPO AT YOUR OWN
LEGAL RISK!

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
panel serve 'examples/basic.py' --autoreload --show
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

```bash
panel build src/panel_vegafusion
```

## Test

```bash
pytest tests
```

## References

- [VegaFusion](https://github.com/vegafusion/vegafusion)
- [Feature Request for Panel Support](https://github.com/vegafusion/vegafusion/issues/62)

## Issues Identified

- https://github.com/holoviz/panel/issues/3149
- https://github.com/holoviz/param/issues/597