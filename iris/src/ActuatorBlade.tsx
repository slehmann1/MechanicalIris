import React from "react";

class ActuatorBlade extends React.Component<{
  innerRadius: number;
  outerRadius: number;
  pinCount: number;
  slotInnerRadius: number;
  slotOuterRadius: number;
  slotWidth: number;
  rotationAngle: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  COLOUR = "blue";
  render() {
    return (
      <g>
        <circle
          cx={this.props.offset.x}
          cy={this.props.offset.y}
          r={this.props.innerRadius * this.props.scale.x}
          fill="None"
          stroke={this.COLOUR}
        />
        <circle
          cx={this.props.offset.x}
          cy={this.props.offset.y}
          r={this.props.outerRadius * this.props.scale.x}
          fill="None"
          stroke={this.COLOUR}
        />
        {this.range(0, this.props.pinCount, 1).map((num, i) =>
          this.renderSlot(
            this.props.slotWidth,
            this.props.slotOuterRadius,
            this.props.slotInnerRadius,
            ((2 * Math.PI) / this.props.pinCount) * i,
            this.props.offset,
            this.props.scale
          )
        )}
      </g>
    );
  }
  range(start, end, step) {
    const numbers: number[] = [];
    for (let i = start; i < end; i += step) {
      numbers.push(i);
    }
    return numbers;
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

    console.log(rotation);
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
export default ActuatorBlade;
