// Mock implementation of shared-cascading-slot module
const setup = jest.fn();
const onContainerCreated = jest.fn();
const onContainerDestroyed = jest.fn();
const install = jest.fn();
const uninstall = jest.fn();
const FEATURE_NAME = 'cascading-slot';
const defaultFeatures = [];

// Export everything as a namespace to match the import * as CascadingSlotFeature style
export {
    setup,
    onContainerCreated,
    onContainerDestroyed,
    install,
    uninstall,
    FEATURE_NAME,
    defaultFeatures,
}; 