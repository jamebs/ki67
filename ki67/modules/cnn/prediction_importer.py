from dataclasses import dataclass

from magda.module import Module
from magda.decorators import finalize, produce, register

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.predictions import Predictions
from ki67.services.io import DataIO


@produce(Predictions)
@register('PredictionImporter')
@finalize
class PredictionImporter(Module.Runtime):
    """ Prediction Importer """

    @dataclass(frozen=True)
    class Parameters:
        filename: str

    @with_logger
    def run(self, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        io = DataIO(shared.target, request.uid)
        predictions = io.dataframe.load(params.filename)

        return Predictions(
            uid=request.uid,
            predictions=predictions,
        )
