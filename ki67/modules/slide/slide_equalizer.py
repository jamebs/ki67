from dataclasses import dataclass

import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept
from skimage import exposure

from ki67.interfaces.slide import Slide


@accept(Slide)
@produce(Slide)
@register('SlideEqualizer')
@finalize
class SlideEqualizer(Module.Runtime):
    """ Slide Eqalizer Module"""

    @dataclass(frozen=True)
    class Parameters:
        kernel: int

    def run(self, data: Module.ResultSet, **kwargs):
        params = self.Parameters(**self.parameters)
        slide: Slide = data.get(Slide)

        image = slide.image / 255.0
        image = exposure.equalize_adapthist(image, params.kernel)
        image = (image * 255).astype(np.uint8)

        return Slide(
            uid=slide.uid,
            filepath=slide.filepath,
            image=image,
            x_offset=slide.x_offset,
            y_offset=slide.y_offset,
        )
