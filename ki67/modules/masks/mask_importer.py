from dataclasses import dataclass

from magda.module import Module
from magda.decorators import finalize, produce, register

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.mask import Mask
from ki67.services.io import DataIO


@produce(Mask)
@register('MaskImporter')
@finalize
class MaskImporter(Module.Runtime):
    """ Mask Importer """

    @dataclass(frozen=True)
    class Parameters:
        filename: str

    @with_logger
    def run(self, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        io = DataIO(shared.target, request.uid)
        mask = io.array.load(params.filename)

        return Mask(
            uid=request.uid,
            data=mask,
            # vrange is not supported!
        )
