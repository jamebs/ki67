from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from skimage import color, exposure, morphology, filters
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.mask import Mask
from ki67.interfaces.fuzzy_cells import FuzzyCells


@accept(Slide, Mask)
@produce(FuzzyCells)
@register('FuzzySegmentator')
@finalize
class FuzzySegmentator(Module.Runtime):
    """ Fuzzy Segmentator """
    HEMATOX_CHANNEL = 0
    DAB_CHANNEL = 2

    @dataclass(frozen=True)
    class Parameters:
        min_area: int
        threshold_positive: Optional[float] = field(default=None)
        threshold_all: Optional[float] = field(default=None)
        factor: float = field(default=0.5)

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        params = self.Parameters(**self.parameters)
        slide: Slide = data.get(Slide)
        mask: Mask = data.get(Mask)

        hed = color.rgb2hed(slide.image[:, :, :3])

        positive, pmask = self._segmentate(
            exposure.rescale_intensity(
                hed[:, :, self.DAB_CHANNEL],
                out_range=(0, 1),
            ),
            mask.data,
            bias=params.threshold_positive,
        )

        all, _ = self._segmentate(
            exposure.rescale_intensity(
                hed[:, :, self.HEMATOX_CHANNEL],
                out_range=(0, 1),
            ),
            mask.data,
            pmask,
            bias=params.threshold_all,
        )

        return FuzzyCells(
            uid=slide.uid,
            data={
                FuzzyCells.CellType.POSITIVE: positive,
                FuzzyCells.CellType.ALL: all,
            },
        )

    def _segmentate(self, layer, mask, mask_add=None, bias=None):
        params = self.Parameters(**self.parameters)
        bf = params.factor

        t = filters.thresholding.threshold_otsu(layer)
        t = (bf * bias) + ((1 - bf) * t) if bias is not None else t

        cells_mask = np.where(layer >= t, True, False)
        if mask_add is not None:
            cells_mask = np.bitwise_or(cells_mask, mask_add.astype(np.bool))

        cells_mask = morphology.remove_small_objects(
            cells_mask,
            params.min_area,
        )
        cells_mask = morphology.binary_closing(cells_mask, np.ones((5, 5)))

        result = cells_mask.astype(float) * mask
        return result, cells_mask
