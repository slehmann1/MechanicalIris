import React from "react";
import { BladeComponent, Blade } from "./Blade.tsx";

class IrisVisual extends React.Component<{
  bladeRadius: number;
  subtendedAngle: number;
  bladeWidth: number;
  pinDiameter: number;
  pinnedRadius: number;
  clearance: number;
  numBlades: number;
}> {
  render() {
    const blades: Blade[] = [];
    for (let i = 0; i < this.props.numBlades; i++) {
      const c = {
        x:
          this.props.pinnedRadius *
          Math.cos(((Math.PI * 2) / this.props.numBlades) * i),
        y:
          this.props.pinnedRadius *
          Math.sin(((Math.PI * 2) / this.props.numBlades) * i),
      };
      blades.push(
        new Blade(
          this.props.bladeRadius,
          this.props.subtendedAngle,
          0,
          c,
          this.props.pinDiameter + this.props.clearance,
          this.props.bladeWidth,
          i
        )
      );
    }
    return (
      <div className="iris-visual">
        <svg>
          <g>
            {blades.map((blade, i) => (
              <BladeComponent blade={blade} key={i}></BladeComponent>
            ))}
          </g>
        </svg>
      </div>
    );
  }
}
export default IrisVisual;
