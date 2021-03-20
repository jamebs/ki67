import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Type, Optional

from magda.module import ModuleFactory
from magda.pipeline.parallel import init, ParallelPipeline

from ki67.common import Request, Context


class BasePipeline(ABC):
    def __init__(self, factory: Type[ModuleFactory] = ModuleFactory):
        init()
        self.factory = factory
        self.pipeline: Optional[ParallelPipeline] = None

    @property
    def context(self) -> Context:
        return Context()

    @abstractmethod
    def build(self, *args, **kwargs):
        raise NotImplementedError()

    async def run(self, requests: List[Request]):
        tasks = {
            asyncio.create_task(self.pipeline.run(req))
            for req in requests
        }

        finished = 0
        total = len(tasks)

        while len(tasks) > 0:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )
            tasks = pending
            finished += len(done)

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(
                '\u001B[33m'
                f'[{now}] '
                '\u001B[34m'
                'Pipeline: '
                '\u001B[1;32m'
                f'Done {finished} of {total}'
                '\u001B[22;39m'
            )

        await self.pipeline.close()
