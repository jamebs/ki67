import numpy as np
from skimage import draw, morphology
from magda.module import Module
from magda.decorators import finalize, accept, produce, register

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.markers import Markers
from ki67.interfaces.mask import Mask


@accept(Slide, Markers)
@produce(Mask)
@register('MarkersRoi')
@finalize
class MarkersRoi(Module.Runtime):
    """ Markers ROI """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        markers: Markers = data.get(Markers)

        mask = np.zeros(slide.image.shape[:2], dtype=bool)

        for _, marker in markers.markers.iterrows():
            x, y = marker['x'], marker['y']
            yy, xx = draw.disk(
                center=(int(y), int(x)),
                radius=24,
                shape=mask.shape[:2],
            )
            mask[yy, xx] = True

        mask = morphology.binary_closing(
            image=mask,
            selem=morphology.selem.rectangle(48, 48),
        )
        mask = morphology.binary_closing(
            image=mask,
            selem=morphology.selem.disk(24),
        )
        return Mask(uid=slide.uid, data=mask.astype(float))
