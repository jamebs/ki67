import asyncio
import logging
import json
from glob import glob
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List

import pandas as pd
from magda.pipeline.parallel import init

from ki67.pipelines.config import ConfigPipeline
from ki67.common import Request


logging.basicConfig(
    level=logging.INFO
)

CONFIG_DIR = Path('ki67/pipelines/configs')
SHARDS = ['amy', 'ben', 'charlie', 'ensemble']
SIZES = [48, 96, 192]

thresholds_file = Path('data/experiments/thresholds.csv')
THRESHOLDS = (
    pd.read_csv('data/experiments/thresholds.csv', index_col=0)
    if thresholds_file.exists()
    else pd.DataFrame()
)


@dataclass
class ConfigParams:
    size: int = 0
    model: str = 'null'
    stride: int = 16
    margin: int = 0
    equalizer_kernel: int = 64
    threshold_positive: float = 0.0
    threshold_relevant: float = 0.0
    training_stride: int = field(init=False)
    mask_kernel: int = field(init=False)
    min_area: int = field(init=False)

    def __post_init__(self):
        self.min_area = self.size * self.size
        self.training_stride = self.size
        self.mask_kernel = self.size // 6


def get_all_slides():
    return [
        Request(uid=Path(f).stem)
        for f in glob('data/source/*.png')
    ]


def get_shard_slides(shard):
    with open(f'data/experiments/config.json') as fp:
        data = json.load(fp)

    slides = data['testing']
    slides += data['shards'][shard] if shard != 'ensemble' else []
    return [Request(uid=s) for s in slides]


async def main(runners: Dict[str, List[ConfigParams]]):
    for config, runs in runners.items():
        for params in runs:
            print(
                f'\n CONFIG: {config}'
                f'\n SIZE: {params.size}'
                f'\n MODEL/SHARD: {params.model}\n'
            )
            pipe = ConfigPipeline()
            await pipe.build(CONFIG_DIR / config, asdict(params))
            await pipe.run(
                get_shard_slides(params.model)
                if params.model != 'null'
                else get_all_slides()
            )


if __name__ == '__main__':
    init()
    asyncio.run(main({
        # # == Before training ==
        # # -- common --
        'slides-markers.pipe.yml': [ConfigParams()],
        'thresholding.pipe.yml': [ConfigParams()],
        'segmentation-identity.pipe.yml': [ConfigParams()],

        # # -- per size --
        'fragments.pipe.yml': [
            ConfigParams(size=size)
            for size in SIZES
        ],
        'evaluation-fragments.pipe.yml': [
            ConfigParams(size=size)
            for size in SIZES
        ],

        # # == After Training ==
        # 'evaluation-cnn-single.pipe.yml': [
        #     ConfigParams(size=size, model=model)
        #     for size in SIZES
        #     for model in ['amy', 'ben', 'charlie']
        # ],
        # 'evaluation-cnn-ensemble.pipe.yml': [
        #     ConfigParams(size=size, model='ensemble')
        #     for size in SIZES
        # ],
        # 'masks.pipe.yml': [
        #     ConfigParams(size=size, model=model)
        #     for size in SIZES
        #     for model in SHARDS
        # ],
        # 'segmentation.pipe.yml': [
        #     ConfigParams(size=size, model=model)
        #     for size in SIZES
        #     for model in SHARDS
        # ],
        # 'segmentation-biased.pipe.yml': [
        #     ConfigParams(
        #         size=size,
        #         model=model,
        #         threshold_positive=THRESHOLDS.loc[model, 'positive'],
        #         threshold_relevant=THRESHOLDS.loc[model, 'relevant'],
        #     )
        #     for size in SIZES
        #     for model in SHARDS
        # ],
    }))
