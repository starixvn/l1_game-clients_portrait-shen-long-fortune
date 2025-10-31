import gc from "@sg/game-client-base";
import { LogStore } from "db://shared-components/game/scripts/stores/log-store";
import { sharedContainer } from "../../scripts/shared-container";
import { settings } from "./game-settings";
import { NullErrorHandlers } from "./null-errors-handlers";
import * as CommonSlotFeature from "db://shared-common-slot/index";
import * as CascadingSlotFeature from "db://shared-cluster-cascading/index";
export const containerOptions: gc.IContainerOptions = {
    globalContainer: sharedContainer,
    onContainerCreated: (container) => {
        container.bind(gc.GameConfigs.GameSetting).toConstantValue(settings);
        container.bind(LogStore).to(LogStore);

        container.bind(gc.Error.ErrorHandlers).to(NullErrorHandlers);
    },
    features: [CascadingSlotFeature, CommonSlotFeature, gc.BetDetailsNew, ...gc.defaultFeatures],
};
