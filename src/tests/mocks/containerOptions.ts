import { IContainerOptions } from "@sg/game-client-base";
import { Container } from "inversify";

const mockContainer = {
    id: "mock",
    parent: null,
    options: {},
    _middleware: [],
    bind: jest.fn(),
    unbind: jest.fn(),
    isBound: jest.fn(),
    rebind: jest.fn(),
    unbindAll: jest.fn(),
    isBoundNamed: jest.fn(),
    get: jest.fn(),
    getTagged: jest.fn(),
    getNamed: jest.fn(),
    getAll: jest.fn(),
    getAllTagged: jest.fn(),
    getAllNamed: jest.fn(),
    resolve: jest.fn(),
} as unknown as Container;

export const containerOptions: IContainerOptions = {
    globalContainer: mockContainer,
    onContainerCreated: jest.fn(),
    features: [],
    disabledFeatures: []
}; 