import React from "react";

class DiameterOutline extends React.Component<{
  diameter: number;
  xPosition: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  UNIT = "mm";
  TEXT_MARGIN_LEFT = 10;
  TEXT_MARGIN_TOP = 5;
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

        <line
          x1={this.props.xPosition * this.props.scale.x + this.props.offset.x}
          y1={
            (-this.props.diameter / 2) * this.props.scale.y +
            this.props.offset.y
          }
          x2={this.props.xPosition * this.props.scale.x + this.props.offset.x}
          y2={
            (this.props.diameter / 2) * this.props.scale.y + this.props.offset.y
          }
          markerEnd="url(#arrow)"
          markerStart="url(#arrow)"
          className="arrow"
        />
        <line
          x1={this.props.offset.x}
          y1={
            (this.props.diameter / 2) * this.props.scale.y + this.props.offset.y
          }
          x2={this.props.xPosition * this.props.scale.x + this.props.offset.x}
          y2={
            (this.props.diameter / 2) * this.props.scale.y + this.props.offset.y
          }
          className="leader-line"
        />
        <line
          x1={this.props.offset.x}
          y1={
            (-this.props.diameter / 2) * this.props.scale.y +
            this.props.offset.y
          }
          x2={this.props.xPosition * this.props.scale.x + this.props.offset.x}
          y2={
            (-this.props.diameter / 2) * this.props.scale.y +
            this.props.offset.y
          }
          className="leader-line"
        />
        <circle
          cx={this.props.offset.x}
          cy={this.props.offset.y}
          r={(this.props.diameter / 2) * this.props.scale.x}
          fill="None"
          className="diameter-outline"
        ></circle>
        <text
          x={
            this.props.xPosition * this.props.scale.x +
            this.props.offset.x +
            this.TEXT_MARGIN_LEFT
          }
          y={this.props.offset.y + this.TEXT_MARGIN_TOP}
          className="arrow-text"
        >
          {this.getDimensionText(this.props.diameter)}
        </text>
      </g>
    );
  }
  getDimensionText(dimension: number) {
    return (
      "⌀" + (Math.round(dimension * 1000) / 1000).toFixed(3) + " " + this.UNIT
    );
  }
}

export default DiameterOutline;
