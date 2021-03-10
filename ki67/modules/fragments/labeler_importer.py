from dataclasses import dataclass

from magda.module import Module
from magda.decorators import finalize, produce, register

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.labels import Labels
from ki67.services.io import DataIO


@produce(Labels)
@register('LabelerImporter')
@finalize
class LabelerImporter(Module.Runtime):
    """ Labeler Importer """

    @dataclass(frozen=True)
    class Parameters:
        filename: str
        margin: int

    @with_logger
    def run(self, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        io = DataIO(shared.target, request.uid)
        fragments = io.dataframe.load(params.filename)

        return Labels(
            uid=request.uid,
            fragments=fragments,
            margin=params.margin,
        )
