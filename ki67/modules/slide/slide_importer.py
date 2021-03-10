from dataclasses import dataclass

from magda.module import Module
from magda.decorators import finalize, produce, register

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.services.io import DataIO


@produce(Slide)
@register('SlideImporter')
@finalize
class SlideImporter(Module.Runtime):
    """ Slide Importer """

    @dataclass(frozen=True)
    class Parameters:
        filename: str

    @with_logger
    def run(self, request: Request, **kwargs):
        shared = Shared(**self.shared_parameters)
        params = self.Parameters(**self.parameters)

        io = DataIO(shared.target, request.uid)
        image = io.image.load(params.filename)

        return Slide(
            uid=request.uid,
            filepath=io.image.filepath(params.filename),
            image=image,
        )
