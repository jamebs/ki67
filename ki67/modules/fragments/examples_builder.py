import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.labels import Labels
from ki67.interfaces.train_examples import TrainExamples


@accept(Slide, Labels)
@produce(TrainExamples)
@register('ExamplesBuilder')
@finalize
class ExamplesBuilder(Module.Runtime):
    """ Examples Builder """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        labels: Labels = data.get(Labels)

        export_labels = labels.fragments['labels'].to_numpy()
        export_data = np.stack(
            labels.fragments.apply(
                lambda row: slide.image[
                    row['y1']:row['y2'],
                    row['x1']:row['x2']
                ],
                axis=1,
            ),
        )

        return TrainExamples(
            uid=slide.uid,
            data=export_data,
            labels=export_labels,
        )
