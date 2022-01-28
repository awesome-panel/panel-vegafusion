# panel-vegafusion

WORK IN PROGRESS. NOT WORKING

Provides a [VegaFusion](https://github.com/vegafusion/vegafusion) component (pane) for Panel to enable interactive big data apps using Vega or Altair.

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
pip install -e[all]
```

## Develop

The Panel `VegaFusion` pane is in the `src\panel_vegafusion\__init__.py`.

Its being developed using Panels [ReactiveHTML](https://panel.holoviz.org/user_guide/Custom_Components.html#reactivehtml-components).

For now you can serve a test example with hot reload via

```bash
panel serve 'src\panel_vegafusion\__init__.py' --autoreload --show
```

You can compare to the original Jupyter VegaFusion reference example via

```bash
jupyter lab tests/reference_example.ipynb
```

This might be useful for understanding how VegaFusion works.

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