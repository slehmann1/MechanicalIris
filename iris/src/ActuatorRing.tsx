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
    const tabAngle = Geometry.getChordSubtendedAngle(
      this.props.tabWidth,
      this.props.outerRadius
    );
    const handleCoords = this.getHandleCoords(
      tabAngle,
      this.props.rotationAngle,
      this.props.outerRadius,
      this.props.tabHeight
    );
    return (
      <g>
        <circle
          cx={this.props.offset.x}
          cy={this.props.offset.y}
          r={this.props.innerRadius * this.props.scale.x}
          fill="None"
          stroke={this.COLOUR}
        />
        <path
          d={this.genArcPath(
            this.props.outerRadius,
            0,
            {
              x:
                this.props.outerRadius *
                Math.cos(this.props.rotationAngle - tabAngle / 2),
              y:
                this.props.outerRadius *
                Math.sin(this.props.rotationAngle - tabAngle / 2),
            },
            {
              x:
                this.props.outerRadius *
                Math.cos(this.props.rotationAngle + tabAngle / 2),
              y:
                this.props.outerRadius *
                Math.sin(this.props.rotationAngle + tabAngle / 2),
            }
          )}
          stroke={this.COLOUR}
          fill="none"
        />

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
        {this.createHandle(handleCoords, this.props.scale, this.props.offset)}
      </g>
    );
  }
  getHandleCoords(
    tabAngle: number,
    rotationAngle: number,
    outerRadius: number,
    tabHeight: number
  ) {
    const c1 = {
      x: outerRadius * Math.cos(rotationAngle - tabAngle / 2),
      y: outerRadius * Math.sin(rotationAngle - tabAngle / 2),
    };
    const c2 = {
      x: outerRadius * Math.cos(rotationAngle + tabAngle / 2),
      y: outerRadius * Math.sin(rotationAngle + tabAngle / 2),
    };
    const c3 = {
      x: (outerRadius + tabHeight) * Math.cos(rotationAngle - tabAngle / 2),
      y: (outerRadius + tabHeight) * Math.sin(rotationAngle - tabAngle / 2),
    };
    const c4 = {
      x: (outerRadius + tabHeight) * Math.cos(rotationAngle + tabAngle / 2),
      y: (outerRadius + tabHeight) * Math.sin(rotationAngle + tabAngle / 2),
    };

    return [c1, c2, c3, c4];
  }
  createHandle(
    handleCoords: { x: number; y: number }[],
    scale: { x: number; y: number },
    offset: { x: number; y: number }
  ) {
    const r = Geometry.euclideanDistance(handleCoords[2], handleCoords[3]) / 2;
    const d =
      "M" +
      (handleCoords[0].x * scale.x + offset.x) +
      " " +
      (handleCoords[0].y * scale.y + offset.y) +
      "L" +
      (handleCoords[2].x * scale.x + offset.x) +
      " " +
      (handleCoords[2].y * scale.y + offset.y) +
      "A" +
      r * this.props.scale.x +
      " " +
      r * this.props.scale.x +
      " " +
      0 +
      " 0 1 " +
      (handleCoords[3].x * scale.x + offset.x) +
      " " +
      (handleCoords[3].y * scale.y + offset.y) +
      "L" +
      (handleCoords[3].x * scale.x + offset.x) +
      " " +
      (handleCoords[3].y * scale.y + offset.y) +
      "L" +
      (handleCoords[1].x * scale.x + offset.x) +
      " " +
      (handleCoords[1].y * scale.y + offset.y);
    return <path stroke={this.COLOUR} fill="none" d={d}></path>;
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
  genArcPath(
    r: number,
    angle: number,
    start: { x: number; y: number },
    end: { x: number; y: number }
  ) {
    let string =
      "M " +
      (start.x * this.props.scale.x + this.props.offset.x) +
      " " +
      (start.y * this.props.scale.y + this.props.offset.y);
    string +=
      "A" +
      r * this.props.scale.x +
      " " +
      r * this.props.scale.x +
      " " +
      (angle * 180) / Math.PI +
      " 1 0 " +
      (end.x * this.props.scale.x + this.props.offset.x) +
      " " +
      (end.y * this.props.scale.y + this.props.offset.y);
    return string;
  }
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
