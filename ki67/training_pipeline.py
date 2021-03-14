from magda import ConfigReader
from magda.module import ModuleFactory
from magda.pipeline import SequentialPipeline

from ki67.common import Request, Context
import ki67.modules as modules


class TrainingPipeline:
    def __init__(self, factory=ModuleFactory):
        self.factory = factory

    @property
    def context(self) -> Context:
        return Context()

    async def build(self, config_path):
        with open(config_path) as config:
            self.pipeline: SequentialPipeline.Runtime = (
                await ConfigReader.read(
                    config=config,
                    module_factory=self.factory,
                    context=self.context,
                )
            )

    async def run(self, request: Request):
        output = self.pipeline.run(request)
        print(output)
        self.pipeline.close()
