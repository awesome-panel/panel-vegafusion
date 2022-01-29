// See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
// See https://docs.bokeh.org/en/latest/docs/reference/core/properties.html
import * as p from "@bokehjs/core/properties"

const CHART_WRAPPER_CLASS = 'chart-wrapper';

// The view of the Bokeh extension/ HTML element
// Here you can define how to render the model as well as react to model changes or View events.
export class VegaFusionView extends HTMLBoxView {
    model: VegaFusion
    containerElement: HTMLElement
    viewElement: HTMLElement

    connect_signals(): void {
        super.connect_signals()

        this.connect(this.model.properties.spec.change, () => {
            this.render();
        })
    }

    async render(): Promise<void> {
        console.log("render")
        console.log("spec", this.model.spec)
        console.log("verbose", this.model.verbose)
        console.log("indent", this.model.indent)
        console.log("debounce_wait", this.model.debounce_wait)
        console.log("debounce_max_waith", this.model.debounce_max_wait)
        console.log("full_vega_spec", this.model.full_vega_spec)
        console.log("client_vega_spec", this.model.client_vega_spec)
        console.log("server_vega_spec", this.model.server_vega_spec)
        console.log("comm_plan", this.model.comm_plan)
        console.log("_request", this.model._request)
        console.log("_response", this.model._response)
        console.log(this.model)
        this.el.style.background="red"

        const { render_vegafusion } = await import("vegafusion-wasm");
        console.log(render_vegafusion)
        
        super.render()
        
        this.containerElement = document.createElement("div")
        this.viewElement = document.createElement("div");
        
        this.containerElement.appendChild(this.viewElement)
        this.containerElement.classList.add(CHART_WRAPPER_CLASS);
        
        this.el.appendChild(this.containerElement)
    }
}

export namespace VegaFusion {
    export type Attrs = p.AttrsOf<Props>
    export type Props = HTMLBox.Props & {
        spec: p.Property<string>,
        verbose: p.Property<boolean>,
        indent: p.Property<number>,
        debounce_wait: p.Property<number>,
        debounce_max_wait: p.Property<number|null>,
        full_vega_spec : p.Property<string|null>,
        client_vega_spec : p.Property<string|null>,
        server_vega_spec : p.Property<string|null>,
        comm_plan : p.Property<string|null>,
        _request: p.Property<string>,
        _response: p.Property<string>,
    } 
}

export interface VegaFusion extends VegaFusion.Attrs { }

// The Bokeh .ts model corresponding to the Bokeh .py model
export class VegaFusion extends HTMLBox {
    properties: VegaFusion.Props

    constructor(attrs?: Partial<VegaFusion.Attrs>) {
        super(attrs)
    }
    
    static __module__ = "panel_vegafusion.models.vegafusion_model"

    static init_VegaFusion(): void {
        this.prototype.default_view = VegaFusionView;

        this.define<VegaFusion.Props>(({Boolean, Int, String, Nullable, Number}) => ({
            spec: [String, ""],
            verbose: [Boolean, false],
            indent: [Int, 2],
            debounce_wait: [Number, 30],
            debounce_max_wait: [Nullable(Number), 60],
            full_vega_spec: [Nullable(String), null],
            client_vega_spec: [Nullable(String), null],
            server_vega_spec: [Nullable(String), null],
            comm_plan: [Nullable(String), null],
            _request: [String, ""],
            _response: [String, ""],
        }))
    }
}