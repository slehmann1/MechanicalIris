import React from "react";
class BladeComponent extends React.Component<{
  blade: Blade;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  render() {
    return (
      <g>
        {this.render_hole(this.props.blade.c_coords)}
        {this.render_hole(this.props.blade.a_coords)}
        {this.props.blade.arc_params.map((arc_coords, i) => (
          <path
            key={i}
            d={this.genPath(arc_coords)}
            stroke="black"
            fill="none"
          />
        ))}
      </g>
    );
  }
  genPath(arc_coords: {
    r: number;
    angle: number;
    start: { x: number; y: number };
    end: { x: number; y: number };
  }) {
    let string =
      "M " +
      (arc_coords.start.x * this.props.scale.x + this.props.offset.x) +
      " " +
      (arc_coords.start.y * this.props.scale.y + this.props.offset.y);
    string +=
      "A" +
      arc_coords.r * this.props.scale.x +
      " " +
      arc_coords.r * this.props.scale.x +
      " " +
      (arc_coords.angle * 180) / Math.PI +
      " 0 1 " +
      (arc_coords.end.x * this.props.scale.x + this.props.offset.x) +
      " " +
      (arc_coords.end.y * this.props.scale.y + this.props.offset.y);
    return string;
  }

  render_hole(coords: { x: number; y: number }) {
    return (
      <circle
        cx={coords.x * this.props.scale.x + this.props.offset.x}
        cy={coords.y * this.props.scale.y + this.props.offset.y}
        r={this.props.blade.hole_diameter / 2}
      />
    );
  }
}

class Blade {
  a_coords: { x: number; y: number };
  c_coords: { x: number; y: number };
  arc_params: {
    r: number;
    angle: number;
    start: { x: number; y: number };
    end: { x: number; y: number };
  }[];
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
    this.arc_params = [
      // TODO: Instead of offsetting relative to center of iris, blades should be offset radially relative to the centerpoint of the blade
      this.getArcCoords(
        radius,
        this.offsetRadially(this.a_coords, blade_width / 2),
        this.offsetRadially(this.c_coords, blade_width / 2)
      ),
      this.getArcCoords(
        radius,
        this.offsetRadially(this.a_coords, -blade_width / 2),
        this.offsetRadially(this.c_coords, -blade_width / 2)
      ),

      this.getArcCoords(
        blade_width / 2,
        this.offsetRadially(this.c_coords, blade_width / 2),
        this.offsetRadially(this.c_coords, -blade_width / 2)
      ),
      this.getArcCoords(
        blade_width / 2,
        this.offsetRadially(this.a_coords, -blade_width / 2),
        this.offsetRadially(this.a_coords, blade_width / 2)
      ),
    ];
  }
  offsetRadially(coord: { x: number; y: number }, radialOffset: number) {
    const angle = Math.atan2(coord.y, coord.x);
    return {
      x: coord.x + radialOffset * Math.cos(angle),
      y: coord.y + radialOffset * Math.sin(angle),
    };
  }

  getArcCoords(
    radius: number,
    a: { x: number; y: number },
    b: { x: number; y: number }
  ): {
    r: number;
    angle: number;
    start: { x: number; y: number };
    end: { x: number; y: number };
  } {
    const angle = Math.atan2(a.y - b.y, a.x - b.x);

    return {
      r: radius,
      angle: angle,
      start: a,
      end: b,
    };
  }
}
export { BladeComponent, Blade };
