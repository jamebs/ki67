from typing import Tuple
import numpy as np
import tensorflow as tf


class Record:
    feature_description = {
        'data': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }

    def __init__(self, data: np.ndarray, label: bool):
        self.data = tf.io.encode_png(data)
        self.label = int(label)

    def serialize(self):
        proto = tf.train.Example(
            features=tf.train.Features(
                feature={
                    'data': self._bytes_feature(self.data),
                    'label': self._int64_feature(self.label),
                }
            )
        )
        return proto.SerializeToString()

    @classmethod
    def parse(cls, proto, shape) -> Tuple[tf.Tensor, tf.Tensor]:
        example = tf.io.parse_single_example(proto, cls.feature_description)
        data = tf.io.decode_png(example['data'])
        data = tf.cast(data, dtype=tf.float32) * (1.0 / 255.0)
        data = tf.ensure_shape(data, shape)
        data = tf.clip_by_value(data, 0.0, 1.0)
        label = tf.cast(example['label'], dtype=tf.bool)
        label = tf.reshape(label, (1,))
        return data, label

    @staticmethod
    def _bytes_feature(value):
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _float_feature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    @staticmethod
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
