import numpy as np
from skimage.exposure.exposure import rescale_intensity
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.fuzzy_cells import FuzzyCells
from ki67.interfaces.image import Image


@accept(Slide, FuzzyCells)
@produce(Image)
@register('FuzzyCellsPreview')
@finalize
class FuzzyCellsPreview(Module.Runtime):
    """ Fuzzy Cells Preview """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        cells: FuzzyCells = data.get(FuzzyCells)

        positive = cells.data[FuzzyCells.CellType.POSITIVE]
        all = cells.data[FuzzyCells.CellType.ALL]

        img = slide.image.copy()
        img = img / 255.0
        img = img * 0.5
        img[:, :, 0] += rescale_intensity(positive, out_range=(0, 1)) * 0.5
        img[:, :, 1] += rescale_intensity(all, out_range=(0, 1)) * 0.5
        img = np.clip(img, 0.0, 1.0)
        img = (img * 255).astype(np.uint8)

        return Image(
            uid=slide.uid,
            data=img,
        )
