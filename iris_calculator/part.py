from abc import abstractmethod

from iris_calculator.dxf import DXF


class Part:
    def __init__(self, colour, file_name):
        self._colour = colour
        self.file_name = file_name
        self.shapes = []

    def save_dxf(self):
        dxf = DXF()
        for shape in self.shapes:
            if not shape.construction_line:
                dxf.add_shape(shape)

        dxf.save(self._DXF_FILE_NAME)

    @abstractmethod
    def build_shapes(self, **kwargs):
        pass
