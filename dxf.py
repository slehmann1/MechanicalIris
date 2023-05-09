import ezdxf
import numpy as np
from ezdxf import units

from geometry import Arc, Coordinate


class DXF:
    def __init__(self) -> None:
        self.doc = ezdxf.new(setup=True)
        self.doc.units = units.MM
        self.modelspace = self.doc.modelspace()

    def add_shape(self, shape):
        shape.add_to_dxf(self)

    def save(self, file_name):
        self.doc.saveas(file_name)
