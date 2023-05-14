import React from "react";
class BladeComponent extends React.Component<{
  blade: Blade;
}> {
  render() {
    return (
      <g>
        {this.render_hole(this.props.blade.c_coords)}
        {this.render_hole(this.props.blade.a_coords)}
      </g>
    );
  }

  render_hole(coords: { x: number; y: number }) {
    return (
      <circle
        cx={coords.x}
        cy={coords.y}
        r={this.props.blade.hole_diameter / 2}
      />
    );
  }
}

class Blade {
  a_coords: { x: number; y: number };
  c_coords: { x: number; y: number };
  hole_diameter: number;
  id: number;
  constructor(
    radius: number,
    subtended_angle: number,
    theta_a: number,
    c_coords: { x: number; y: number },
    hole_diameter: number,
    blade_width: number,
    id: number
  ) {
    this.c_coords = c_coords;
    this.hole_diameter = hole_diameter;
    this.id = id;

    const ac = 2 * radius * Math.sin(subtended_angle);
    this.a_coords = {
      x: c_coords.x - Math.cos(theta_a) * ac,
      y: c_coords.y - Math.sin(theta_a) * ac,
    };
  }
}
export { BladeComponent, Blade };
