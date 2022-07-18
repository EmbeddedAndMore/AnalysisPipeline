import json

import numpy as np
from celery import Celery
from kombu.serialization import register


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {"__type__": "__np.ndarray__", "content": obj.tolist()}
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def data_decoder(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__np.ndarray__":
            return np.array(obj["content"])
    return obj


def data_dumps(obj):
    return json.dumps(obj, cls=NumpyArrayEncoder)


def data_loads(obj):
    return json.loads(obj, object_hook=data_decoder)


serializer_name = "NumpySerializer"

register(serializer_name, data_dumps, data_loads, content_type="application/x-myjson", content_encoding="utf-8")

CeleryApp = Celery(
    "pipeline_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    accept_content=["NumpySerializer"],
    task_serializer="NumpySerializer",
    result_serializer="NumpySerializer",
)


CeleryApp.conf.update(
    imports=[
        "app.cum_sum_pipeline.cum_sum_pipeline",
    ]
)
