# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
# Modifications Copyright 2021 Jakub Blaszczyk.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
""" The modified Keras implementation of DenseNet121.

Modifications:
- refactor of the original Keras model class
- reduced the batch normalization momentum
"""
from typing import Tuple
import tensorflow as tf


class DenseNet:
    bn_axis = (
        3 if tf.keras.backend.image_data_format() == 'channels_last'
        else 1
    )

    @classmethod
    def _dense_block(cls, x, blocks, name):
        for i in range(blocks):
            x = cls._conv_block(x, 32, name=name + '_block' + str(i + 1))
        return x

    @classmethod
    def _transition_block(cls, x, reduction, name):
        x = tf.keras.layers.BatchNormalization(
            axis=cls.bn_axis,
            epsilon=1.001e-5,
            momentum=0.1,
            name=name + '_bn')(x)
        x = tf.keras.layers.Activation('relu', name=name + '_relu')(x)
        x = tf.keras.layers.Conv2D(
            int(tf.keras.backend.int_shape(x)[cls.bn_axis] * reduction),
            kernel_size=1,
            use_bias=False,
            name=name + '_conv')(x)
        x = tf.keras.layers.AveragePooling2D(
            pool_size=2,
            strides=2,
            name=name + '_pool')(x)
        return x

    @classmethod
    def _conv_block(cls, x, growth_rate, name):
        x1 = tf.keras.layers.BatchNormalization(
            axis=cls.bn_axis,
            epsilon=1.001e-5,
            momentum=0.1,
            name=name + '_0_bn')(x)
        x1 = tf.keras.layers.Activation('relu', name=name + '_0_relu')(x1)
        x1 = tf.keras.layers.Conv2D(
            4 * growth_rate,
            kernel_size=1,
            use_bias=False,
            name=name + '_1_conv')(x1)
        x1 = tf.keras.layers.BatchNormalization(
            axis=cls.bn_axis,
            epsilon=1.001e-5,
            momentum=0.1,
            name=name + '_1_bn')(x1)
        x1 = tf.keras.layers.Activation('relu', name=name + '_1_relu')(x1)
        x1 = tf.keras.layers.Conv2D(
            growth_rate,
            kernel_size=3,
            padding='same',
            use_bias=False,
            name=name + '_2_conv')(x1)
        x = tf.keras.layers.Concatenate(
            axis=cls.bn_axis,
            name=name + '_concat')([x, x1])
        return x

    @classmethod
    def _DenseNet(cls, blocks, img_input):
        x = tf.keras.layers.ZeroPadding2D(padding=((3, 3), (3, 3)))(img_input)
        x = tf.keras.layers.Conv2D(
            64, 7,
            strides=2,
            use_bias=False,
            name='conv1/conv')(x)
        x = tf.keras.layers.BatchNormalization(
            axis=cls.bn_axis,
            epsilon=1.001e-5,
            momentum=0.1,
            name='conv1/bn')(x)
        x = tf.keras.layers.Activation('relu', name='conv1/relu')(x)
        x = tf.keras.layers.ZeroPadding2D(padding=((1, 1), (1, 1)))(x)
        x = tf.keras.layers.MaxPooling2D(3, strides=2, name='pool1')(x)

        x = cls._dense_block(x, blocks[0], name='conv2')
        x = cls._transition_block(x, 0.5, name='pool2')
        x = cls._dense_block(x, blocks[1], name='conv3')
        x = cls._transition_block(x, 0.5, name='pool3')
        x = cls._dense_block(x, blocks[2], name='conv4')
        x = cls._transition_block(x, 0.5, name='pool4')
        x = cls._dense_block(x, blocks[3], name='conv5')

        x = tf.keras.layers.BatchNormalization(
            axis=cls.bn_axis,
            epsilon=1.001e-5,
            momentum=0.1,
            name='bn')(x)
        x = tf.keras.layers.Activation('relu', name='relu')(x)

        x = tf.keras.layers.GlobalAveragePooling2D(name='avg_pool')(x)
        x = tf.keras.layers.Dense(1, activation='sigmoid', name='logits')(x)

        model = tf.keras.models.Model(img_input, x, name='densenet')
        return model

    @classmethod
    def create(cls, shape: Tuple[int, int, int]):
        """ DenseNet121 """
        img_input = tf.keras.layers.Input(shape)
        model = cls._DenseNet([6, 12, 24, 16], img_input)
        return model
