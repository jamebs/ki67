import numpy as np
from skimage import segmentation
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.cells import Cells
from ki67.interfaces.image import Image


@accept(Slide, Cells)
@produce(Image)
@register('CellsPreview')
@finalize
class CellsPreview(Module.Runtime):
    """ Cells Preview """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        cells: Cells = data.get(Cells)

        positive = cells.data[Cells.CellType.POSITIVE].labels
        all = cells.data[Cells.CellType.ALL].labels

        img = slide.image.copy()
        img = segmentation.mark_boundaries(
            image=img,
            label_img=all,
            color=(1, 1, 0),
            mode='thick',
        )
        img = segmentation.mark_boundaries(
            image=img,
            label_img=positive,
            color=(1, 0, 0),
            mode='thick',
        )
        img = (img * 255).astype(np.uint8)

        return Image(
            uid=slide.uid,
            data=img,
        )
