import asyncio
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

    async def build(self, config_path: Path):
        with open(config_path) as config:
            self.pipeline: ParallelPipeline.Runtime = await ConfigReader.read(
                config=config,
                module_factory=self.factory,
                context=self.context,
            )

    async def run(self, requests: List[Request]):
        await asyncio.gather(*[
            asyncio.create_task(self.pipeline.run(req))
            for req in requests
        ])
