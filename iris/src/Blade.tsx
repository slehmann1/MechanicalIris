import React from "react";
import { Geometry } from "./Geometry.ts";

class BladeComponent extends React.Component<{
  blade: Blade;
  offset: { x: number; y: number };
  scale: { x: number; y: number };
}> {
  render() {
    return (
      <g>
        {this.renderHole(this.props.blade.cCoords)}
        {this.renderHole(this.props.blade.aCoords)}
        {this.props.blade.arcParams.map((arcCoords, i) => (
          <path
            key={i}
            d={this.genArcPath(arcCoords)}
            stroke="black"
            fill="none"
          />
        ))}
      </g>
    );
  }

  /**
   *
   * @param arcCoords Details the arc to be represented
   * @returns String representing an arc in SVG format
   */
  genArcPath(arcCoords: {
    r: number;
    angle: number;
    start: { x: number; y: number };
    end: { x: number; y: number };
  }) {
    let string =
      "M " +
      (arcCoords.start.x * this.props.scale.x + this.props.offset.x) +
      " " +
      (arcCoords.start.y * this.props.scale.y + this.props.offset.y);
    string +=
      "A" +
      arcCoords.r * this.props.scale.x +
      " " +
      arcCoords.r * this.props.scale.x +
      " " +
      (arcCoords.angle * 180) / Math.PI +
      " 0 1 " +
      (arcCoords.end.x * this.props.scale.x + this.props.offset.x) +
      " " +
      (arcCoords.end.y * this.props.scale.y + this.props.offset.y);
    return string;
  }

  renderHole(coords: { x: number; y: number }) {
    return (
      <circle
        cx={coords.x * this.props.scale.x + this.props.offset.x}
        cy={coords.y * this.props.scale.y + this.props.offset.y}
        r={this.props.blade.holeDiameter / 2}
      />
    );
  }
}

class Blade {
  aCoords: { x: number; y: number };
  cCoords: { x: number; y: number };
  arcParams: {
    r: number;
    angle: number;
    start: { x: number; y: number };
    end: { x: number; y: number };
  }[];
  holeDiameter: number;
  id: number;
  LOG_VALS = false;
  constructor(
    radius: number,
    subtendedAngle: number,
    thetaA: number,
    cCoords: { x: number; y: number },
    holeDiameter: number,
    bladeWidth: number,
    id: number,
    centreRotationAngle: number
  ) {
    const ac = Math.abs(2 * radius * Math.sin(subtendedAngle / 2));
    this.aCoords = {
      x: cCoords.x + Math.cos(thetaA) * ac,
      y: cCoords.y + Math.sin(thetaA) * ac,
    };
    this.cCoords = Geometry.rotateAboutOrigin(cCoords, centreRotationAngle);
    this.aCoords = Geometry.rotateAboutOrigin(
      this.aCoords,
      centreRotationAngle
    );
    this.holeDiameter = holeDiameter;
    this.id = id;
    const bladeCentre = Geometry.getCentre(this.aCoords, this.cCoords, radius);

    const bladePoints: { x: number; y: number }[] = [
      Geometry.offsetRadially(this.aCoords, bladeCentre, bladeWidth / 2),
      Geometry.offsetRadially(this.cCoords, bladeCentre, bladeWidth / 2),
      Geometry.offsetRadially(this.aCoords, bladeCentre, -bladeWidth / 2),
      Geometry.offsetRadially(this.cCoords, bladeCentre, -bladeWidth / 2),
    ];

    this.arcParams = [
      //Outer Arc
      this.getArcCoords(
        radius + bladeWidth / 2,
        bladePoints[0],
        bladePoints[1]
      ),
      //Inner Arc
      this.getArcCoords(
        radius - bladeWidth / 2,
        bladePoints[2],
        bladePoints[3]
      ),

      this.getArcCoords(bladeWidth / 2, bladePoints[1], bladePoints[3]),
      this.getArcCoords(bladeWidth / 2, bladePoints[2], bladePoints[0]),
    ];
    if (this.LOG_VALS) {
      console.log("A " + this.aCoords.x + " " + this.aCoords.y);
      console.log("C " + this.cCoords.x + " " + this.cCoords.y);
      console.log("Theta a " + (thetaA * 180) / Math.PI);
      console.log("Radius " + radius);
      console.log("Subtended Angle: " + (subtendedAngle * 180) / Math.PI);
      console.log("AC " + ac);
    }
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
