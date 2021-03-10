from dataclasses import dataclass

import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.fragments import Fragments
from ki67.interfaces.markers import Markers
from ki67.interfaces.labels import Labels


@accept(Slide, Fragments, Markers)
@produce(Labels)
@register('Labeler')
@finalize
class Labeler(Module.Runtime):
    """ Labeler """

    @dataclass(frozen=True)
    class Parameters:
        margin: int

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        params = self.Parameters(margin=int(self.parameters['margin']))

        slide: Slide = data.get(Slide)
        fragments: Fragments = data.get(Fragments)
        markers: Markers = data.get(Markers)

        mask = self._get_mask(slide, markers)
        labels = fragments.fragments.apply(
            lambda r: self._get_label(r, mask, params.margin),
            axis=1,
        )

        return Labels(
            uid=slide.uid,
            fragments=fragments.fragments.assign(labels=labels),
            margin=params.margin,
        )

    def _get_mask(self, slide: Slide, markers: Markers) -> np.ndarray:
        yy, xx, _ = slide.image.shape
        mask = np.zeros(shape=(yy, xx)).astype(bool)
        for marker in markers.markers.itertuples():
            mask[marker.y, marker.x] = True
        return mask

    def _get_label(self, row, mask: np.ndarray, margin: int) -> bool:
        fragment_mask = mask[
            row['y1']+margin:row['y2']-margin,
            row['x1']+margin:row['x2']-margin,
        ]
        return np.max(fragment_mask) > 0
