from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from skimage import color, exposure, morphology, filters, measure
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.interfaces.slide import Slide
from ki67.interfaces.mask import Mask
from ki67.interfaces.cells import Cells


@accept(Slide, Mask)
@produce(Cells)
@register('Segmentator')
@finalize
class Segmentator(Module.Runtime):
    """ Segmentator """
    HEMATOX_CHANNEL = 0
    DAB_CHANNEL = 2

    @dataclass(frozen=True)
    class Parameters:
        min_area: int
        threshold_positive: Optional[float] = field(default=None)
        threshold_relevant: Optional[float] = field(default=None)
        factor: float = field(default=0.5)

    def run(self, data: Module.ResultSet, **kwargs):
        params = self.Parameters(**self.parameters)
        slide: Slide = data.get(Slide)
        mask: Mask = data.get(Mask)

        hed = color.rgb2hed(slide.image[:, :, :3])
        hed_mask = mask.data.astype(bool)
        if np.all(~hed_mask):
            hed_mask[:] = True

        positive = self._segmentate(
            exposure.rescale_intensity(
                hed[:, :, self.DAB_CHANNEL],
                out_range=(0, 1),
            ),
            hed_mask,
            bias=params.threshold_positive,
        )

        all = self._segmentate(
            exposure.rescale_intensity(
                hed[:, :, self.HEMATOX_CHANNEL],
                out_range=(0, 1),
            ),
            hed_mask,
            positive.mask,
            bias=params.threshold_relevant,
        )

        return Cells(
            uid=slide.uid,
            data={
                Cells.CellType.POSITIVE: positive,
                Cells.CellType.ALL: all,
            },
        )

    def _segmentate(self, layer, mask, mask_add=None, bias=None):
        params = self.Parameters(**self.parameters)
        bf = params.factor

        t = filters.threshold_otsu(layer[mask])
        t = (bf * bias) + ((1 - bf) * t) if bias is not None else t

        cells_mask = (layer * mask)
        cells_mask = np.where(cells_mask >= t, True, False)
        if mask_add is not None:
            cells_mask = np.bitwise_or(cells_mask, mask_add)

        cells_mask = morphology.remove_small_objects(
            cells_mask,
            params.min_area,
        )
        cells_mask = morphology.binary_closing(cells_mask, np.ones((5, 5)))
        labels = measure.label(cells_mask, connectivity=2).astype(np.uint16)

        return Cells.CellsLabel(
            mask=cells_mask,
            labels=labels,
            threshold=t,
        )
