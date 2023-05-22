import React from "react";

class BasePlate extends React.Component<{
  pinCount: number;
  holeDiameter: number;
  pinnedRadius: number;
  rotationAngle: number;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  COLOUR = "green";
  render() {
    return (
      <g>
        {this.range(0, this.props.pinCount, 1).map((num, i) =>
          this.renderHole(
            this.props.holeDiameter / 2,
            this.props.pinnedRadius,
            ((2 * Math.PI) / this.props.pinCount) * i +
              this.props.rotationAngle,
            this.props.offset,
            this.props.scale,
            this.COLOUR,
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

  renderHole(
    circleRadius: number,
    pitchCircleRadius: number,
    angle: number,
    offset: { x: number; y: number },
    scale: { x: number; y: number },
    colour: string,
    key: number
  ) {
    const centreCoords = {
      x: pitchCircleRadius * Math.cos(angle) * scale.x + offset.x,
      y: pitchCircleRadius * Math.sin(angle) * scale.y + offset.y,
    };

    return (
      <circle
        cx={centreCoords.x}
        cy={centreCoords.y}
        r={circleRadius * scale.x}
        fill="None"
        stroke={colour}
        key={key}
      />
    );
  }
}

export default BasePlate;
