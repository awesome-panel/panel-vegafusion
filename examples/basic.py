import panel as pn
from panel_vegafusion.vega_fusion_pane import VegaFusion
from panel_vegafusion._utils import get_chart

VegaFusion.enable()

VegaFusion(object=get_chart()).servable()