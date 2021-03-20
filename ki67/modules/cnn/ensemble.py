from dataclasses import dataclass
from typing import Dict

import numpy as np
from magda.module import Module
from magda.decorators import finalize, produce, register, accept

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.predictions import Predictions


@accept(Predictions)
@produce(Predictions)
@register('EnsemblePredictions')
@finalize
class EnsemblePredictions(Module.Runtime):
    """ Ensemble Predictions """

    @dataclass
    class Parameters:
        classifiers: Dict[str, str]

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        params = self.Parameters(**self.parameters)
        predictions = data.filter(Predictions)

        base: Predictions = predictions[0].result
        df = base.predictions[['x1', 'x2', 'y1', 'y2', 'labels']]

        for x in predictions:
            name = params.classifiers[x.name]
            result: Predictions = x.result
            df[name] = result.predictions['prediction']

        df['prediction'] = (
            df[list(params.classifiers.values())]
            .mean(axis=1)
            .round()
            .astype(np.bool)
        )

        return Predictions(
            uid=base.uid,
            predictions=df,
        )
