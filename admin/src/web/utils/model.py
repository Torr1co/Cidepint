from enum import Enum


def enum_mutation(model: dict, mutation=None):
    dicc = {}
    for c in model:
        if mutation is not None and isinstance(model[c], Enum):
            dicc[c] = mutation(model[c])
        else:
            dicc[c] = model[c]
    return dicc


def array_mutation(model: dict, mutation=None):
    dicc = {}
    for c in model:
        if mutation is not None and isinstance(model[c], list):
            dicc[c] = mutation(model[c])
        else:
            dicc[c] = model[c]
    return dicc
