from dataclasses import dataclass

import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

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

    @dataclass(frozen=True)
    class Parameters:
        stride: int

    def run(self, data: Module.ResultSet, *args, **kwargs):
        params = self.Parameters(**self.parameters)
        slide: Slide = data.get(Slide)

        x_border = np.all(slide.image == 255, (0, 2))
        y_border = np.all(slide.image == 255, (1, 2))
        x, y = np.argmin(x_border), np.argmin(y_border)
        w, h = np.sum(x_border == False), np.sum(y_border == False)  # noqa

        x += (w % params.stride) // 2
        y += (h % params.stride) // 2
        w -= w % params.stride
        h -= h % params.stride

        return Slide(
            uid=slide.uid,
            filepath=slide.filepath,
            image=slide.image[y:y+h, x:x+w],
            x_offset=x,
            y_offset=y,
        )
