from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import tensorflow as tf
from tqdm import tqdm
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.common import Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.labels import Labels
from ki67.interfaces.predictions import Predictions
from .utils.model import DenseNet


@accept(Slide, Labels)
@produce(Predictions)
@register('CNN')
@finalize
class CNN(Module.Runtime):
    """ CNN """

    @dataclass(frozen=True)
    class Parameters:
        model: str
        batch: int = field(default=128)

    def bootstrap(self):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)
        img_shape = (shared.fragment, shared.fragment, 3)

        self.model = DenseNet.create(shape=img_shape)
        self.model.load_weights(params.model)

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)
        labels: Labels = data.get(Labels)

        dataset, indices = self._get_dataset(slide, labels)
        raw_predictions = self.model.predict(dataset)
        y = raw_predictions.flatten().round().astype(bool)
        predictions = self._prepare_df(
            labels.fragments,
            pd.Series(y, index=indices, dtype=bool),
        )

        return Predictions(
            uid=slide.uid,
            predictions=predictions,
        )

    def _get_data_generator(self, image: np.ndarray, fragments: pd.DataFrame):
        def data_generator():
            for _, f in fragments.iterrows():
                sample = image[f['y1']:f['y2'], f['x1']:f['x2']] * (1. / 255)
                yield sample.astype(np.float32)
        return data_generator, fragments.index

    def _get_dataset(self, slide: Slide, labels: Labels):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)
        img_shape = (shared.fragment, shared.fragment, 3)

        ds, indices = self._get_data_generator(slide.image, labels.fragments)
        dataset = tf.data.Dataset.from_generator(
            generator=ds,
            output_signature=tf.TensorSpec(img_shape, dtype=tf.float32),
        )
        dataset = dataset.batch(params.batch)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        return dataset, indices

    def _prepare_df(self, dataset: pd.DataFrame, predictions: pd.Series):
        return dataset.assign(prediction=predictions)
