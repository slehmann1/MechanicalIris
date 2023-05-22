import time

import matplotlib.patches as patch
import matplotlib.pyplot as plt
import numpy as np

from iris_calculator.actuator_ring import ActuatorRing
from iris_calculator.base_plate import BasePlate
from iris_calculator.blade import Blade


class Iris:
    _SLEEP_TIME = 0.0001
    _COLOUR = "red"
    _ENDLESS_DRAW = True

    def __init__(
        self,
        blade_count,
        blade_angle,
        aperture_inner_radius,
        aperture_outer_radius,
        blade_width,
        peg_radius,
        peg_clearance,
    ):
        self.blade_count = blade_count
        self.aperture_inner_radius = aperture_inner_radius
        self.aperture_outer_radius = aperture_outer_radius
        self.blade_width = blade_width
        self.peg_radius = peg_radius
        self.peg_clearance = peg_clearance
        self.pinned_radius = aperture_outer_radius + blade_width * 2
        self.BC = self.pinned_radius * 1.07

        self.fig = plt.figure()
        self.axs = self.fig.gca()
        self.fig.set_size_inches(10, 10)

        blade_radius = self.pinned_radius * 0.96
        tab_width = self.blade_width / 2
        tab_height = self.blade_width / 2

        if blade_width > blade_radius:
            raise ValueError("Blade width too large")

        self.blades = [
            Blade(
                2 * np.pi / blade_count * i,
                blade_angle,
                self.pinned_radius,
                blade_radius,
                self.BC,
                self.peg_radius,
                self.blade_width,
            )
            for i in range(blade_count)
        ]

        self.blades[0].set_theta_a_domain(
            aperture_inner_radius + blade_width / 2,
            aperture_outer_radius + blade_width / 2,
        )

        self.domain = self.blades[0].theta_a_range

        # Only calculate blade state for one blade, others are rotated duplicates
        initial_blade_state = self.blades[0].calc_blade_states(
            self.domain[0], self.domain[1]
        )
        print(f"Blade radius: {blade_radius} Pinned radius: {self.pinned_radius}")
        print(f"Theta a domain: {self.domain}")
        self.blade_states = [
            [
                initial_blade_state[ii].rotated_copy(2 * np.pi / self.blade_count * i)
                for ii in range(len(initial_blade_state))
            ]
            for i in range(self.blade_count)
        ]
        min_A_rad, max_A_rad = self.calc_A_range(initial_blade_state)

        min_rad = min(min_A_rad - peg_radius * 2, self.aperture_outer_radius)
        max_rad = max(self.pinned_radius + peg_radius * 2, max_A_rad + peg_radius * 2)

        self.base_plate = BasePlate(
            min_rad,
            max_rad,
            self.pinned_radius,
            self.peg_clearance + self.peg_radius,
            self.blade_count,
            tab_width,
            tab_height,
        )

        self.actuator_ring = ActuatorRing(
            min_rad,
            max_rad,
            self.peg_radius + self.peg_clearance,
            self.blade_count,
            min_A_rad,
            max_A_rad,
            tab_width,
            tab_height,
        )

    def calc_A_range(self, blade_states):
        start_A_rad = np.inf
        end_A_rad = -np.inf
        for blade_state in blade_states:
            if blade_state.A.magnitude() < start_A_rad:
                start_A_rad = blade_state.A.magnitude()
            if blade_state.A.magnitude() > end_A_rad:
                end_A_rad = blade_state.A.magnitude()

        return start_A_rad, end_A_rad

    def drawIris(self):
        plt.show(block=False)
        i = 0
        multiplier = 1
        act_ring_angle = self.blade_states[0][0].A.angle()

        while i < len(self.blade_states[0]):
            rotation_angle = self.blade_states[0][i].C.angle()

            plt.cla()
            for blade_index in range(len(self.blades)):
                self.blades[blade_index].build_shapes(
                    blade_state=self.blade_states[blade_index][i]
                )
                self.blades[blade_index].draw(
                    self.axs, self.blade_states[blade_index][i]
                )

            self.base_plate.draw(self.axs, rotation_angle)
            self.actuator_ring.draw(self.axs, act_ring_angle)

            self.axs.add_patch(
                patch.Circle(
                    (0, 0), self.aperture_outer_radius, color=self._COLOUR, fill=False
                )
            )

            self.axs.add_patch(
                patch.Circle(
                    (0, 0), self.aperture_inner_radius, color=self._COLOUR, fill=False
                )
            )

            self.axs.add_patch(
                patch.Circle((0, 0), 0.01, color=self._COLOUR, fill=True)
            )

            self.axs.axis(
                [
                    -self.aperture_outer_radius * 2.5,
                    self.aperture_outer_radius * 2.5,
                    -self.aperture_outer_radius * 2.5,
                    self.aperture_outer_radius * 2.5,
                ]
            )
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(self._SLEEP_TIME)

            i += 1 * multiplier

            if self._ENDLESS_DRAW and i in [len(self.blade_states[0]) - 1, 0]:
                multiplier *= -1
        plt.close()

        self.blades[0].save_dxf()
        self.base_plate.save_dxf()
        self.actuator_ring.save_dxf()


# iris = Iris(6, np.pi, 10, 30, 10, 2, 0.5)
# iris.drawIris()
