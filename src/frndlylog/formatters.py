import json
import logging

from datetime import date, datetime
from importlib import import_module
from typing import Any, Sequence

from . import constants


def select(record: logging.LogRecord, fields: list[str]) -> dict:
    return {getattr(record, field) for field in fields}


class FrndlyJsonEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(self, obj)


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        encoder: str = "frndlylog.formatters.FrndlyJsonEncoder",
        fields: Sequence[str] = constants.DEFAULT_FIELDS,
        **kwargs
    ):
        *module_name, class_name = encoder.split(".")
        encoder_module = import_module(module_name.join("."))

        self.encoder = getattr(encoder_module, class_name)
        self.fields = fields
        self.kwargs = kwargs

    def format(self, record: logging.LogRecord) -> str:
        # This sets the %(message)s attribute on the record
        super().format(record)
        obj = select(record, self.fields)
        return json.dumps(obj, cls=self.encoder, **self.kwargs)


