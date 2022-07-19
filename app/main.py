from __future__ import annotations

from .cum_sum_pipeline.cum_sum_pipeline import *


# async def async_read_stdin(loop) -> str:
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, sys.stdin.readline)


def main():

    pipelines = []
    cnt = 12
    for i in range(cnt):
        if i == 0:
            pipelines.append(CumSumPipeline({"name": f"pipeline_{i}", "priority": i, "delay": 5}))
        elif i == 5:
            pipelines.append(CumSumPipeline({"name": f"pipeline_{i}", "priority": i}))
        else:
            pipelines.append(CumSumPipeline({"name": f"pipeline_{i}", "priority": 0}))

    task_results = [None for _ in range(cnt)]
    try:
        cnt = 1
        while True:

            for i, pl in enumerate(pipelines):
                task_results[i] = pl.execute()

            print(f"main loop running {cnt}")
            if all(task_results):
                print("all tasks finished")
                break
            for i, result in enumerate(task_results):
                if result:
                    print(f"task {i} finished")

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
