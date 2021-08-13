import numpy as np
from skimage import draw
from magda.module import Module
from magda.decorators import finalize, accept, produce, register

from ki67.interfaces.slide import Slide
from ki67.interfaces.markers import Markers
from ki67.interfaces.image import Image


@accept(Slide, Markers)
@produce(Image)
@register('MarkersPreview')
@finalize
class MarkersPreview(Module.Runtime):
    """ Markers Preview """

    colors = [None, (255, 0, 0), (0, 255, 0)]

    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        markers: Markers = data.get(Markers)

        preview = slide.image[:, :, :3].copy()
        marker_radius = np.max(preview.shape) // 250
        marker_size = np.max(preview.shape) // 650

        for _, marker in markers.markers.iterrows():
            for i in range(marker_size):
                yy, xx = draw.circle_perimeter(
                    marker.y,
                    marker.x,
                    marker_radius - i,
                    shape=preview.shape,
                )
                preview[yy, xx] = self.colors[marker.type]
        return Image(uid=slide.uid, data=preview)
