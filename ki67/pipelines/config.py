from pathlib import Path
from typing import Dict

from magda import ConfigReader
from magda.pipeline.parallel import ParallelPipeline

import ki67.modules as modules
from .base import BasePipeline


class ConfigPipeline(BasePipeline):
    async def build(self, config_path: Path, params: Dict):
        with open(config_path) as config:
            self.pipeline: ParallelPipeline.Runtime = await ConfigReader.read(
                config=config.read(),
                module_factory=self.factory,
                config_parameters=params,
                context=self.context,
            )
