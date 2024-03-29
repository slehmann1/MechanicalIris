import React from "react";
import { Geometry } from "./Geometry.ts";

class ActuatorRing extends React.Component<{
  pinCount: number;
  slotInnerRadius: number;
  slotOuterRadius: number;
  slotWidth: number;
  rotationAngle: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  static COLOUR = "#9fbfcc";
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
            this.props.scale,
            i
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
    scale: { x: number; y: number },
    key: number
  ) {
    const centreCoords = {
      x: innerRadius,
      y: -width / 2,
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
        stroke={ActuatorRing.COLOUR}
        transform={rotation}
        vectorEffect="non-scaling-stroke"
        key={key}
      />
    );
  }
}
export default ActuatorRing;
