async function getPanelVegaFusion(){
  const { render_vegafusion } = await import("vegafusion-wasm");
  const { compile } = await import("vega-lite");

  let panelVegaFusion = {
    render_vegafusion: render_vegafusion,
    compile: compile
  };
  return panelVegaFusion
}

window.getPanelVegaFusion = getPanelVegaFusion
export {};
