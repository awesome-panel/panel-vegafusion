# panel-vegafusion

WORK IN PROGRESS

Provides a VegaFusion component (pane) for Panel to enable interactive big data apps using Vega or Altair

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

## Test

```bash
pytest tests
```
