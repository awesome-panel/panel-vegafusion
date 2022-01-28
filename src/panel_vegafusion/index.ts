import * as VegaFusionExtensions from "./models"
export {VegaFusionExtensions as VegaFusion}

import {register_models} from "@bokehjs/base"
register_models(VegaFusionExtensions as any)