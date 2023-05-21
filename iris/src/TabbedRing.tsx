import React from "react";
import { Geometry } from "./Geometry.ts";

class TabbedRing extends React.Component<{
  innerRadius: number;
  outerRadius: number;
  rotationAngle: number;
  tabWidth: number;
  tabHeight: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
  colour: string;
  children: React.ReactNode;
}> {
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
          stroke={this.props.colour}
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
          stroke={this.props.colour}
          fill="none"
        />

        {this.createHandle(
          handleCoords,
          this.props.scale,
          this.props.offset,
          this.props.colour
        )}
        {this.props.children}
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
    offset: { x: number; y: number },
    colour: string
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
    return <path stroke={colour} fill="none" d={d}></path>;
  }
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
}
export default TabbedRing;
