from dataclasses import dataclass

import numpy as np
from magda.module import Module
from magda.decorators import finalize, accept, register
from skimage import exposure, color

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger, get_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.markers import Markers
from ki67.interfaces.image import Image
from ki67.interfaces.mask import Mask
from ki67.interfaces.fragments import Fragments
from ki67.interfaces.labels import Labels
from ki67.interfaces.predictions import Predictions
from ki67.interfaces.train_examples import TrainExamples
from ki67.services.io import DataIO


@accept(
    Slide, Image, Mask,
    Markers, Fragments, Labels, Predictions,
    TrainExamples,
)
@register('Exporter')
@finalize
class Exporter(Module.Runtime):
    """ Exporter """

    def bootstrap(self):
        self.logger = get_logger(self)

    @dataclass(frozen=True)
    class Parameters:
        filename: str

    @with_logger
    def run(self, data: Module.ResultSet, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)
        io = DataIO(shared.target, request.uid)

        self.validate(data)

        if data.has(Slide):
            asset: Slide = data.get(Slide)
            io.image.save(params.filename, asset.image)
        elif data.has(Image):
            asset: Image = data.get(Image)
            io.image.save(params.filename, asset.data)
        elif data.has(Mask):
            mask: Mask = data.get(Mask)
            mask_preview = color.gray2rgb(
                exposure.rescale_intensity(
                    image=mask.data,
                    in_range=mask.vrange,
                    out_range=(0, 255),
                ).astype(np.uint8),
            )
            io.array.save(params.filename, mask.data)
            io.image.save(params.filename, mask_preview)
        elif data.has(Markers):
            asset: Markers = data.get(Markers)
            io.dataframe.save(params.filename, asset.markers, index=False)
        elif data.has(Fragments):
            asset: Fragments = data.get(Fragments)
            io.dataframe.save(params.filename, asset.fragments, index=False)
        elif data.has(Labels):
            asset: Labels = data.get(Labels)
            io.dataframe.save(params.filename, asset.fragments, index=False)
        elif data.has(Predictions):
            asset: Predictions = data.get(Predictions)
            io.dataframe.save(params.filename, asset.predictions, index=False)
        elif data.has(TrainExamples):
            asset: TrainExamples = data.get(TrainExamples)
            io.multiarray.save(
                params.filename,
                data=asset.data,
                labels=asset.labels,
            )
        else:
            self.logger.warn(f'{self.name} Unsupported data type')

    def validate(self, data: Module.ResultSet):
        if len(data) > 1:
            raise Exception(
                f'Exporter [{self.name}] can export '
                'only 1 asset at the same time',
            )
