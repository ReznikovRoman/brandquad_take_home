from __future__ import annotations

import os
from typing import Any, Type, cast

from configurations import values

_NOTSET = object()

_value_classes = {
    str: values.Value,
    int: values.IntegerValue,
    float: values.FloatValue,
    bool: values.BooleanValue,
    list: values.ListValue,
    tuple: values.TupleValue,
    dict: values.DictValue,
}


def from_environ(
    __default: object = _NOTSET, /, *, name: str | None = None, type: Type | object = _NOTSET, **kwargs: Any,
) -> values.Value:
    kwargs["environ"] = True
    kwargs.setdefault("environ_prefix", None)
    if __default is _NOTSET:
        kwargs["environ_required"] = True
    else:
        kwargs["environ_required"] = False
        kwargs["default"] = __default
    if name:
        kwargs["environ_name"] = name
        if os.environ.get("DJANGO_CONFIGURATION", "Prod") == "Lint":
            kwargs["environ_required"] = False
    if type is _NOTSET:
        if __default is _NOTSET or __default is None:
            type = str
        else:
            type = object.__class__(__default)
    type = cast("Type", type)
    return _value_classes[type](**kwargs)
