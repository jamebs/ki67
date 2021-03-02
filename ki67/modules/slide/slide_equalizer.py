import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept
from skimage import exposure

from ki67.common import Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide


@accept(Slide)
@produce(Slide)
@register('SlideEqualizer')
@finalize
class SlideEqualizer(Module.Runtime):
    """ Slide Eqalizer Module"""

    @property
    def shared(self) -> Shared:
        return Shared(**self.shared_parameters)

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        stride = self.shared.stride

        image = slide.image / 255.0
        image = exposure.equalize_adapthist(image, stride * 4)
        image = (image * 255).astype(np.uint8)

        return Slide(
            uid=slide.uid,
            filepath=slide.filepath,
            image=image,
            x_offset=slide.x_offset,
            y_offset=slide.y_offset,
        )
