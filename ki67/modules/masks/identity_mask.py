import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.mask import Mask
from ki67.interfaces.slide import Slide


@accept(Slide)
@produce(Mask)
@register('IdentityMask')
@finalize
class IdentityMask(Module.Runtime):
    """ Identity Mask """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        mask = np.ones(slide.image.shape[:2])
        return Mask(
            uid=slide.uid,
            data=mask,
            vrange=(0, 1),
        )
