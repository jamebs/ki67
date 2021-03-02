from pathlib import Path

from magda.module import Module
from magda.decorators import finalize, produce, register
from skimage import io

from ki67.common import Request, Shared
from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide


@produce(Slide)
@register('SlideLoader')
@finalize
class SlideLoader(Module.Runtime):
    """ Slide Loader """

    @with_logger
    def run(self, request: Request, **kwargs):
        uid = request.uid
        shared = Shared(**self.shared_parameters)

        filepath = Path(shared.source) / f'{uid}.png'
        if not filepath.exists():
            raise Exception(f"{filepath} doesn't exists!")

        image = io.imread(filepath)[:, :, :3]

        return Slide(
            uid=uid,
            filepath=filepath,
            image=image,
        )
