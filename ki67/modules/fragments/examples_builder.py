from dataclasses import dataclass

import tensorflow as tf
from magda.module import Module
from magda.decorators import finalize, register, accept

from ki67.common import Request, Shared
from ki67.interfaces.slide import Slide
from ki67.interfaces.labels import Labels
from ki67.services.io import DataIO
from ki67.services.record import Record


@accept(Slide, Labels)
@register('ExamplesBuilder')
@finalize
class ExamplesBuilder(Module.Runtime):
    """ Examples Builder """

    @dataclass
    class Parameters:
        filename: str

    def run(self, data: Module.ResultSet, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        slide: Slide = data.get(Slide)
        labels: Labels = data.get(Labels)

        io = DataIO(shared.target, request.uid)
        filepath = str(io.tfrecord.filepath(params.filename))

        with tf.io.TFRecordWriter(filepath) as writer:
            for _, row in labels.fragments.iterrows():
                record = Record(
                    data=slide.image[row['y1']:row['y2'], row['x1']:row['x2']],
                    label=row['labels'],
                )
                writer.write(record.serialize())
