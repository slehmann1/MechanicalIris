import React from "react";

class AngularDimension extends React.Component<{
  startAngle: number;
  endAngle: number;
  dimensionRadialPosition: number;
  radialDiameter: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  TEXT_MARGIN_TOP = 25;
  render(): React.ReactNode {
    return (
      <g>
        <defs>
          <marker
            id="arrow"
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
            className="arrow-head"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" />
          </marker>
        </defs>
        <path
          d={this.genArcPath(
            this.props.dimensionRadialPosition * this.props.scale.x,
            {
              x:
                Math.cos(this.props.startAngle) *
                  this.props.dimensionRadialPosition *
                  this.props.scale.x +
                this.props.offset.x,
              y:
                this.props.dimensionRadialPosition * this.props.scale.y +
                this.props.offset.y,
            },
            {
              x:
                Math.cos(this.props.endAngle) *
                  this.props.dimensionRadialPosition *
                  this.props.scale.x +
                this.props.offset.x,
              y:
                this.props.dimensionRadialPosition * this.props.scale.y +
                this.props.offset.y,
            }
          )}
          stroke="black"
          fill="None"
          className="arrow"
          markerEnd="url(#arrow)"
          markerStart="url(#arrow)"
        ></path>

        <line
          x1={
            this.props.radialDiameter *
              Math.cos(this.props.startAngle) *
              this.props.scale.x +
            this.props.offset.x
          }
          y1={
            -this.props.radialDiameter *
              Math.sin(this.props.startAngle) *
              this.props.scale.y +
            this.props.offset.y
          }
          x2={
            this.props.dimensionRadialPosition *
              Math.cos(this.props.startAngle) *
              this.props.scale.x +
            this.props.offset.x
          }
          y2={
            this.props.dimensionRadialPosition * this.props.scale.y +
            this.props.offset.y
          }
          className="leader-line"
        />

        <line
          x1={
            this.props.radialDiameter *
              Math.cos(this.props.endAngle) *
              this.props.scale.x +
            this.props.offset.x
          }
          y1={
            -this.props.radialDiameter *
              Math.sin(this.props.endAngle) *
              this.props.scale.y +
            this.props.offset.y
          }
          x2={
            this.props.dimensionRadialPosition *
              Math.cos(this.props.endAngle) *
              this.props.scale.x +
            this.props.offset.x
          }
          y2={
            this.props.dimensionRadialPosition * this.props.scale.y +
            this.props.offset.y
          }
          className="leader-line"
        />

        <text
          x={
            ((Math.cos(this.props.startAngle) + Math.cos(this.props.endAngle)) /
              2) *
              this.props.dimensionRadialPosition *
              this.props.scale.x +
            this.props.offset.x
          }
          y={
            this.props.dimensionRadialPosition * this.props.scale.y +
            this.props.offset.y +
            this.TEXT_MARGIN_TOP
          }
          className="angle-text"
        >
          {this.getDimensionText(this.props.startAngle, this.props.endAngle)}
        </text>
      </g>
    );
  }
  genArcPath(
    r: number,
    start: { x: number; y: number },
    end: { x: number; y: number }
  ) {
    let string = "M " + start.x + " " + start.y;
    string += "A" + r + " " + r + " " + 0 + " 0 0 " + end.x + " " + end.y;
    return string;
  }
  getDimensionText(startAngle: number, endAngle: number) {
    return (
      (
        Math.round((((endAngle - startAngle) * 180) / Math.PI) * 1000) / 1000
      ).toFixed(3) + "°"
    );
  }
}
export default AngularDimension;
