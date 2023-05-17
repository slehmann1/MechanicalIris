import React from "react";
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
  constructor(
    radius: number,
    subtendedAngle: number,
    thetaA: number,
    cCoords: { x: number; y: number },
    holeDiameter: number,
    bladeWidth: number,
    id: number
  ) {
    this.cCoords = cCoords;
    this.holeDiameter = holeDiameter;
    this.id = id;

    const ac = 2 * radius * Math.sin(subtendedAngle / 2);
    this.aCoords = {
      x: cCoords.x - Math.cos(thetaA) * ac,
      y: cCoords.y - Math.sin(thetaA) * ac,
    };
    const bladeCentre = this.getCentre(this.aCoords, this.cCoords, radius);

    const bladePoints: { x: number; y: number }[] = [
      this.offsetRadially(this.aCoords, bladeCentre, bladeWidth / 2),
      this.offsetRadially(this.cCoords, bladeCentre, bladeWidth / 2),
      this.offsetRadially(this.aCoords, bladeCentre, -bladeWidth / 2),
      this.offsetRadially(this.cCoords, bladeCentre, -bladeWidth / 2),
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
  }

  /**
   * Determines the centrepoint of a circle
   * @param a Coordinate on the circle
   * @param b Coordinate on the circle
   * @param radius Circle radius
   * @returns Coordinate for the centrepoint of the circle
   */
  getCentre(
    a: { x: number; y: number },
    b: { x: number; y: number },
    radius: number
  ) {
    const chordLength = Math.sqrt(
      Math.pow(b.x - a.x, 2) + Math.pow(b.y - a.y, 2)
    );
    let d = 0;
    if (radius > chordLength / 2) {
      d = Math.sqrt(Math.pow(radius, 2) - Math.pow(chordLength / 2, 2));
    } else {
      d = Math.sqrt(Math.pow(chordLength / 2, 2) - Math.pow(radius, 2));
    }
    const midChord = this.linterp(a, b, 0.5);
    const chordAngle = Math.atan2(b.y - a.y, b.x - a.x);
    return {
      x: midChord.x + d * Math.cos(chordAngle + Math.PI / 2),
      y: midChord.y + d * Math.sin(chordAngle + Math.PI / 2),
    };
  }

  /**
   * Linearly interpolates between two 2D coordinates
   * @param a Start coordinate
   * @param b End coordinate
   * @param progress Progress between 0 and 1
   * @returns Linearly interpolated coordinate
   */
  linterp(
    a: { x: number; y: number },
    b: { x: number; y: number },
    progress: number
  ) {
    return { x: a.x + (b.x - a.x) * progress, y: a.y + (b.y - a.y) * progress };
  }

  /**
   * Offsets a coordinate in teh radial direction from another coordinate by a given distance
   * @param coord Coordinate to offset
   * @param centre Centrepoint to radially offset the coordinate from
   * @param radialOffset Amount to radially offset the coordinate
   * @returns Offset coordinate
   */
  offsetRadially(
    coord: { x: number; y: number },
    centre: { x: number; y: number },
    radialOffset: number
  ) {
    const angle = Math.atan2(coord.y - centre.y, coord.x - centre.x);
    return {
      x: coord.x + radialOffset * Math.cos(angle),
      y: coord.y + radialOffset * Math.sin(angle),
    };
  }

  euclideanDistance(a: { x: number; y: number }, b: { x: number; y: number }) {
    return Math.sqrt(Math.pow(b.x - a.x, 2) + Math.pow(b.y - a.y, 2));
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
