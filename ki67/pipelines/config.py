from pathlib import Path

from magda import ConfigReader
from magda.pipeline.parallel import ParallelPipeline

import ki67.modules as modules
from .base import BasePipeline


class ConfigPipeline(BasePipeline):
    def build(self, config_path: Path):
        with open(config_path) as config:
            self.pipeline: ParallelPipeline.Runtime = ConfigReader.read(
                config=config,
                module_factory=self.factory,
                context=self.context,
            )
