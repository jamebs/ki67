import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, expose

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.shards import Shards


@produce(Shards)
@register('Splitter')
@expose()
@finalize
class Splitter(Module.Runtime):
    """ Splitter """

    @dataclass(frozen=True)
    class Parameters:
        shards: List[str]
        testing: int
        experiments: str
        force: bool = field(default=False)

    @with_logger
    def run(self, request: Request, **kwargs):
        params = self.Parameters(**self.parameters)
        config = Path(params.experiments) / request.uid / 'config.json'

        if config.exists() and not params.force:
            data = self.load(config)
        else:
            config.parent.mkdir(parents=True, exist_ok=True)
            data = self.generate(config)

        testing = set(data['testing'])
        shards = data['shards']

        if len(testing) != params.testing or len(shards) != len(params.shards):
            raise Exception('Config is incompatible with parameters!')

        return Shards(
            uid=request.uid,
            testing=testing,
            training={
                key: set(value)
                for key, value in shards.items()
            },
        )

    def load(self, config: Path) -> Shards:
        with open(config) as fh:
            data = json.load(fh)
        return data

    def generate(self, config: Path) -> Shards:
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        total = [
            f.stem
            for f in Path(shared.target).iterdir()
            if f.is_dir()
        ]

        testing: np.ndarray = np.random.choice(total, params.testing, False)
        training = list(set(total).difference(set(testing)))
        shards = np.array_split(training, len(params.shards))

        data = dict(
            testing=list(testing),
            shards={
                name: list(values)
                for name, values in zip(params.shards, shards)
            }
        )

        with open(config, 'w') as fh:
            json.dump(data, fh, indent=2)

        return data
