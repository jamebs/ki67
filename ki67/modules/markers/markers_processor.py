from pathlib import Path
from xml.etree.ElementTree import ElementTree

import pandas as pd
from magda.module import Module
from magda.decorators import finalize, accept, produce, register

from ki67.modules.utils.logging import with_logger
from ki67.interfaces.slide import Slide
from ki67.interfaces.markers import Markers


@accept(Slide)
@produce(Markers)
@register('MarkersProcessor')
@finalize
class MarkersProcessor(Module.Runtime):
    """ Markers Processor """

    @with_logger
    def run(self, data: Module.ResultSet, **kwargs):
        slide: Slide = data.get(Slide)

        parent = Path(slide.filepath).parent
        if (xml_file := parent / f'{slide.uid}.xml').exists():
            markers = self._process_xml(xml_file)
        elif (csv_file := parent / f'{slide.uid}.csv').exists():
            markers = pd.read_csv(csv_file)
        else:
            raise Exception('Bad extension')

        markers['type'] = markers['type'].astype(int)
        markers['x'] = markers['x'].astype(int) - slide.x_offset
        markers['y'] = markers['y'].astype(int) - slide.y_offset

        return Markers(uid=slide.uid, markers=markers)

    @staticmethod
    def _process_xml(file):
        markers = []
        tree = ElementTree().parse(file)
        for marker_group in tree.findall('Marker_Data/Marker_Type'):
            marker_type = marker_group.find('Type').text
            for marker in marker_group.findall('Marker'):
                markers.append(dict(
                    type=marker_type,
                    x=marker.find('MarkerX').text,
                    y=marker.find('MarkerY').text,
                ))
        markers = pd.DataFrame(markers)
        return markers