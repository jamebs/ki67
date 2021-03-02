import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.common import Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide


@accept(Slide)
@produce(Slide)
@register('SlideCropper')
@finalize
class SlideCropper(Module.Runtime):
    """ Slide Cropper Module

    Crop image to remove white border (if exists)
    and adjust to fragmentation stride.

    ImageJ (or other tools) sometimes adds white border
    which is harmful for the further parts of the pipeline.
    We would like to remove these border pixels.

    The second part evenly removes pixels from each
    of the sides to have the image dimension, which
    divides by fragmentation stride completely.
    """

    @property
    def shared(self) -> Shared:
        return Shared(**self.shared_parameters)

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        stride = self.shared.stride

        x_border = np.all(slide.image == 255, (0, 2))
        y_border = np.all(slide.image == 255, (1, 2))
        x, y = np.argmin(x_border), np.argmin(y_border)
        w, h = np.sum(x_border == False), np.sum(y_border == False)  # noqa

        x += (w % stride) // 2
        y += (h % stride) // 2
        w -= w % stride
        h -= h % stride

        return Slide(
            uid=slide.uid,
            filepath=slide.filepath,
            image=slide.image[y:y+h, x:x+w],
            x_offset=x,
            y_offset=y,
        )
