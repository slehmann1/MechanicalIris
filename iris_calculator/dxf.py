import ezdxf
import numpy as np
from ezdxf import units

from iris_calculator.geometry import Arc, Coordinate


class DXF:
    _DXF_LOC = "dxf//"

    def __init__(self) -> None:
        self.doc = ezdxf.new(setup=True)
        self.doc.units = units.MM
        self.modelspace = self.doc.modelspace()

    def add_shape(self, shape):
        shape.add_to_dxf(self)

    def save(self, file_name):
        self.doc.saveas(self._DXF_LOC + file_name)
