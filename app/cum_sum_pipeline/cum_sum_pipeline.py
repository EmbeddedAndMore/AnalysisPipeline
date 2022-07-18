from __future__ import annotations
from time import sleep
from celery import Task
from celery.result import AsyncResult
from ..celery_app import CeleryApp
from ..analysis_base.base import *


class CumSumDataLoader(BaseDataLoader, Task):
    def run(self) -> np.ndarray:
        sleep(1)
        return np.arange(100).reshape(50, 2)


class CumSumProcessor(BaseProcessor, Task):
    def __init__(self) -> None:
        self.current_stage: ProcessorStage = ProcessorStage.PREPROCESS
        self.stage2task = {
            ProcessorStage.PREPROCESS: self.pre_process,
            ProcessorStage.PROCESS: self.process,
            ProcessorStage.POSTPROCESS: self.post_process,
        }

    def pre_process(self, data: np.ndarray) -> np.ndarray:
        sleep(1)
        return data

    def process(self, data: np.ndarray) -> np.ndarray:
        sleep(1)
        return data.cumsum(axis=0)
        # return Process.apply_async(args=(data,), serializer=serializer_name).get()

    def post_process(self, data: np.ndarray) -> np.ndarray:
        sleep(1)
        return data

    def run(self, data: np.ndarray) -> np.ndarray:

        data = self.pre_process(data)
        data1 = self.process(data)
        data2 = self.post_process(data1)
        return data2


cum_sum_loader = CumSumDataLoader()
CeleryApp.register_task(cum_sum_loader)

cum_sum_processor = CumSumProcessor()
CeleryApp.register_task(cum_sum_processor)


class CumSumPipeline(BasePipeline):
    data_loader: CumSumDataLoader
    processor: CumSumProcessor
    config: dict = {}

    def __init__(self, config: dict):
        self.data_loader = cum_sum_loader
        self.processor = cum_sum_processor
        self.config = config
        self.current_state = PipelineStage.PENDING
        self.loader_result: AsyncResult | None = None
        self.processor_result: AsyncResult | None = None

    @property
    def finished(self) -> bool:
        return self.current_state == PipelineStage.FINISHED

    def execute(self) -> bool:

        if self.current_state == PipelineStage.PENDING:
            print(f"{self.config['name']} started.")
            self.current_state = PipelineStage.PROVIDE_DATA
            self.loader_result = self.data_loader.delay()

        elif (
            self.loader_result and self.loader_result.successful() and self.current_state == PipelineStage.PROVIDE_DATA
        ):
            self.current_state = PipelineStage.PROCESS
            self.processor_result = self.processor.delay(data=self.loader_result.get())

        elif (
            self.processor_result and self.processor_result.successful() and self.current_state == PipelineStage.PROCESS
        ):
            self.current_state = PipelineStage.FINALIZE
            self.current_state = PipelineStage.FINISHED

            print("result: ", self.processor_result.get()[:2])
            print(f"{self.config['name']} finished.")

        return self.finished
