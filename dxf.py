import ezdxf
import numpy as np

from geometry import Arc, Coordinate


class DXF:
    def __init__(self) -> None:
        self.doc = ezdxf.new(setup=True)
        self.modelspace = self.doc.modelspace()

    def add_shape(self, shape):
        shape.add_to_dxf(self)

    def save(self, file_name):
        self.doc.saveas(file_name)
