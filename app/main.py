from __future__ import annotations
import celer as celer
from celery import Celery

# import asyncio
import sys

# from asyncio import Task
from .analysis_base.base import PipelineStage
from .cum_sum_pipeline.cum_sum_pipeline import *


# async def async_read_stdin(loop) -> str:
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, sys.stdin.readline)


def main():
    pipeline1, pipeline2 = CumSumPipeline({"name": "pipeline_1"}), CumSumPipeline({"name": "pipeline_2"})

    task1: PipelineStage | None = None
    task2: PipelineStage | None = None
    try:
        cnt = 1
        while True:

            task1 = pipeline1.execute()
            task2 = pipeline2.execute()

            print(f"main loop running {cnt}")
            if task1 and task2:
                print("loop finished.")
                break

            cnt += 1
            sleep(0.5)
            # await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        print("interrupted!")


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    try:
        main()
        # loop.run_until_complete(main(loop))
    except KeyboardInterrupt:
        print("Received exit, exiting")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
