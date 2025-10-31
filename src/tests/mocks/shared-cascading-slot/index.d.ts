/// <reference types="jest" />

declare module "db://shared-cascading-slot/index" {
    export const setup: jest.MockedFunction<any>;
    export const onContainerCreated: jest.MockedFunction<any>;
    export const onContainerDestroyed: jest.MockedFunction<any>;
    export const install: jest.MockedFunction<any>;
    export const uninstall: jest.MockedFunction<any>;
    export const FEATURE_NAME: string;
    export const defaultFeatures: any[];
} 