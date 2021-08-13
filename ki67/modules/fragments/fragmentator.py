from dataclasses import dataclass
import pandas as pd
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.common import Shared
from ki67.interfaces.slide import Slide
from ki67.interfaces.fragments import Fragments


@accept(Slide)
@produce(Fragments)
@register('Fragmentator')
@finalize
class Fragmentator(Module.Runtime):
    """ Fragmentator """

    @dataclass(frozen=True)
    class Parameters:
        step: int

    def run(self, data: Module.ResultSet, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)
        slide: Slide = data.get(Slide)

        size = shared.fragment
        shape = slide.image.shape

        indices = [
            (x, y)
            for x in range(0, shape[1] - size, params.step)
            for y in range(0, shape[0] - size, params.step)
        ]

        return Fragments(
            uid=slide.uid,
            fragments=pd.DataFrame([
                self.create_fragment(x, y, size)
                for x, y in indices
            ]),
        )

    def create_fragment(self, x1, y1, size):
        y2 = y1 + size
        x2 = x1 + size
        return pd.Series(
            data=dict(y1=y1, y2=y2, x1=x1, x2=x2),
            name=f'{y1}_{y2}-{x1}_{x2}',
        )
