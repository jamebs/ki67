import numpy as np
from skimage import exposure
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.predictions import Predictions
from ki67.interfaces.mask import Mask


@accept(Slide, Predictions)
@produce(Mask)
@register('Fuzzificator')
@finalize
class Fuzzificator(Module.Runtime):
    """ Mask Fuzzificator """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        predictions: Predictions = data.get(Predictions)

        df = predictions.predictions

        mask = np.zeros(slide.image.shape[:2])
        for _, entry in df[df.prediction].iterrows():
            mask[entry.y1:entry.y2, entry.x1:entry.x2] += 1
        mask = exposure.rescale_intensity(mask, out_range=(0, 1))

        return Mask(
            uid=slide.uid,
            data=mask,
            vrange=(0, 1),
        )
