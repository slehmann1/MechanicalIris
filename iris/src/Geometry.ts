class Geometry {
  a = 1;
  /**
   * Linearly interpolates between two 2D coordinates
   * @param a Start coordinate
   * @param b End coordinate
   * @param progress Progress between 0 and 1
   * @returns Linearly interpolated coordinate
   */
  static linterp(
    a: { x: number; y: number },
    b: { x: number; y: number },
    progress: number
  ) {
    return { x: a.x + (b.x - a.x) * progress, y: a.y + (b.y - a.y) * progress };
  }
  static euclideanDistance(
    a: { x: number; y: number },
    b: { x: number; y: number }
  ) {
    return Math.sqrt(Math.pow(b.x - a.x, 2) + Math.pow(b.y - a.y, 2));
  }

  /**
   * Determines the centrepoint of a circle
   * @param a Coordinate on the circle
   * @param b Coordinate on the circle
   * @param radius Circle radius
   * @returns Coordinate for the centrepoint of the circle
   */
  static getCentre(
    a: { x: number; y: number },
    b: { x: number; y: number },
    radius: number
  ) {
    const chordLength = this.euclideanDistance(a, b);
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

  static rotateAboutOrigin(
    coordinate: { x: number; y: number },
    angle: number
  ) {
    const magnitude = Geometry.euclideanDistance(coordinate, { x: 0, y: 0 });
    const init_angle = Math.atan2(coordinate.y, coordinate.x);
    return {
      x: magnitude * Math.cos(init_angle + angle),
      y: magnitude * Math.sin(init_angle + angle),
    };
  }

  /**
   * Offsets a coordinate in the radial direction from another coordinate by a given distance
   * @param coord Coordinate to offset
   * @param centre Centrepoint to radially offset the coordinate from
   * @param radialOffset Amount to radially offset the coordinate
   * @returns Offset coordinate
   */
  static offsetRadially(
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

  /**
   * Computes the length of a chord on a circle
   * @param radius Radius of the circle
   * @param subtendedAngle Angle subtended by two points tangent to the circle
   * @returns Length of the chord
   */
  static chordLength(radius: number, subtendedAngle: number) {
    return 2 * radius * Math.sin(subtendedAngle / 2);
  }

  /**
   * Computes the subtended angle for a chord on a circle
   * @param chordLength The length of the chord
   * @param circleRadius The radius of the circle
   * @returns Subtended Angle
   */

  static getChordSubtendedAngle(chordLength: number, circleRadius: number) {
    return 2 * Math.asin(chordLength / 2 / circleRadius);
  }

  /**
   * Determines the point normal to the tangent line between two coordinates at a set distance
   * @param a First coordinate
   * @param b Second coordinate
   * @param normalDistance Normal distance from the tangent line between the two coordinates
   * @returns Coordinate of the point
   */
  static midpointNormal(
    a: { x: number; y: number },
    b: { x: number; y: number },
    normalDistance: number
  ) {
    const midpoint = this.linterp(a, b, 0.5);
    const normalAngle = Math.atan2(b.y - a.y, b.x - a.x) + Math.PI / 2;
    return {
      x: midpoint.x + normalDistance * Math.cos(normalAngle),
      y: midpoint.y + normalDistance * Math.sin(normalAngle),
    };
  }
}
export { Geometry };
