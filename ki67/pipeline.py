import asyncio
from datetime import datetime
from pathlib import Path
from typing import List

from magda import ConfigReader
from magda.module import ModuleFactory
from magda.pipeline.parallel import init, ParallelPipeline

from ki67.common import Request, Context
import ki67.modules as modules


class Pipeline:
    def __init__(self, factory=ModuleFactory):
        init()
        self.factory = factory

    @property
    def context(self) -> Context:
        return Context()

    def build(self, config_path: Path):
        with open(config_path) as config:
            self.pipeline: ParallelPipeline.Runtime = ConfigReader.read(
                config=config,
                module_factory=self.factory,
                context=self.context,
            )

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
