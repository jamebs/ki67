from dataclasses import dataclass

import numpy as np
from skimage import morphology as morph
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.interfaces.mask import Mask


@accept(Mask)
@produce(Mask)
@register('Defuzzificator')
@finalize
class Defuzzificator(Module.Runtime):
    """ Mask Defuzzificator """

    @dataclass(frozen=True)
    class Parameters:
        kernel: int
        min_area: int
        threshold: float

    def run(self, data: Module.ResultSet, **kwargs):
        params = self.Parameters(**self.parameters)
        fuzzy_mask: Mask = data.get(Mask)

        mask = fuzzy_mask.data
        mask = np.where(mask >= params.threshold, True, False).astype(bool)
        mask = morph.binary_closing(mask, morph.disk(params.kernel))
        mask = morph.binary_erosion(mask, morph.disk(params.kernel // 2))
        mask = morph.remove_small_objects(mask, params.min_area)
        mask = mask.astype(np.float)

        return Mask(
            uid=fuzzy_mask.uid,
            data=mask,
            vrange=(0, 1),
        )
