import React from "react";
import { Geometry } from "./Geometry.ts";

class ActuatorRing extends React.Component<{
  innerRadius: number;
  outerRadius: number;
  pinCount: number;
  slotInnerRadius: number;
  slotOuterRadius: number;
  slotWidth: number;
  rotationAngle: number;
  tabWidth: number;
  tabHeight: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  COLOUR = "blue";
  render() {
    return (
      <g>
        {this.range(0, this.props.pinCount, 1).map((num, i) =>
          this.renderSlot(
            this.props.slotWidth,
            this.props.slotOuterRadius,
            this.props.slotInnerRadius,
            ((2 * Math.PI) / this.props.pinCount) * i +
              this.props.rotationAngle,
            this.props.offset,
            this.props.scale
          )
        )}
      </g>
    );
  }

  range(start: number, end: number, step: number) {
    const numbers: number[] = [];
    for (let i = start; i < end; i += step) {
      numbers.push(i);
    }
    return numbers;
  }
  /**
   *
   * @param arcCoords Details the arc to be represented
   * @returns String representing an arc in SVG format
   */

  renderSlot(
    width: number,
    outerRadius: number,
    innerRadius: number,
    angle: number,
    offset: { x: number; y: number },
    scale: { x: number; y: number }
  ) {
    const centreCoords = {
      x: innerRadius,
      y: 0,
    };

    // Translate, scale, and rotate the actuator blade
    const rotation =
      "translate(" +
      offset.x +
      "," +
      offset.y +
      ") rotate(" +
      (angle * 180) / Math.PI +
      ")" +
      "scale(" +
      scale.x +
      "," +
      scale.y +
      ")";

    return (
      <rect
        x={centreCoords.x}
        y={centreCoords.y}
        width={outerRadius - innerRadius}
        height={width}
        fill="None"
        stroke={this.COLOUR}
        transform={rotation}
        vectorEffect="non-scaling-stroke"
      />
    );
  }
}
export default ActuatorRing;
