import numpy as np
from magda.module import Module
from magda.decorators import finalize, accept, produce, register

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.image import Image
from ki67.interfaces.mask import Mask


@accept(Slide, Mask)
@produce(Image)
@register('MarkersRoiPreview')
@finalize
class MarkersRoiPreview(Module.Runtime):
    """ Markers ROI Preview """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        mask: Mask = data.get(Mask)

        image = slide.image.copy()
        mask_data = np.dstack(3 * [mask.data])
        roi = ((0.5 * image) + (0.5 * mask_data * image)).astype(np.uint8)

        return Image(uid=slide.uid, data=roi)
