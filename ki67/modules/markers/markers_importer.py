from dataclasses import dataclass

from magda.decorators import finalize, produce, register
from magda.module import Module

from ki67.common import Request, Shared
from ki67.interfaces.markers import Markers
from ki67.modules.utils.logging import with_logger
from ki67.services.io import DataIO


@produce(Markers)
@register('MarkersImporter')
@finalize
class MarkersImporter(Module.Runtime):
    """ Markers Importer """

    @dataclass(frozen=True)
    class Parameters:
        filename: str

    @with_logger
    def run(self, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        io = DataIO(shared.target, request.uid)
        markers = io.dataframe.load(params.filename)

        return Markers(uid=request.uid, markers=markers)
