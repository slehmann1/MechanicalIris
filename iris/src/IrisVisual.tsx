import React from "react";
import { BladeComponent, Blade } from "./Blade.tsx";

class IrisVisual extends React.Component<
  {
    bladeRadius: number;
    subtendedAngle: number;
    bladeWidth: number;
    pinDiameter: number;
    pinnedRadius: number;
    clearance: number;
    numBlades: number;
    rotationSpeed: number; // rad/s
    minAngle: number;
    maxAngle: number;
  },
  {
    offset: { x: number; y: number };
    scale: { x: number; y: number };
    rotationAngle: number;
  }
> {
  ref?: any;
  interval: any;
  MARGIN = 1;
  REFRESH_FREQUENCY = 15;
  startTime: number;
  constructor(props: any) {
    super(props);
    this.ref = React.createRef();
    this.state = {
      offset: { x: 0, y: 0 },
      scale: { x: 1, y: 1 },
      rotationAngle: 0,
    };
  }

  render() {
    const blades: Blade[] = [];
    const chordLength = this.chordLength(
      this.props.bladeRadius,
      this.props.subtendedAngle
    );

    for (let i = 0; i < this.props.numBlades; i++) {
      const bladeAngle = ((Math.PI * 2) / this.props.numBlades) * i;
      let c = {
        x: this.props.pinnedRadius * Math.cos(this.state.rotationAngle / 2),
        y: this.props.pinnedRadius * Math.sin(this.state.rotationAngle / 2),
      };
      c = this.rotateCoord(c, bladeAngle);
      blades.push(
        new Blade(
          this.props.bladeRadius,
          this.props.subtendedAngle,
          ((Math.PI * 2) / this.props.numBlades) * i + this.state.rotationAngle,
          c,
          this.props.pinDiameter + this.props.clearance,
          this.props.bladeWidth,
          i
        )
      );
    }
    return (
      <div className="iris-visual">
        <svg ref={this.ref} style={{ height: "100%", width: "100%" }}>
          <g>
            {blades.map((blade, i) => (
              <BladeComponent
                blade={blade}
                offset={this.state.offset}
                scale={this.state.scale}
                key={i}
              ></BladeComponent>
            ))}
            <circle
              cx={this.state.offset.x}
              cy={this.state.offset.y}
              r={this.props.pinnedRadius * this.state.scale.x}
              fill="None"
              stroke="black"
            />
          </g>
        </svg>
      </div>
    );
  }

  euclideanDistance(a: { x: number; y: number }, b: { x: number; y: number }) {
    return Math.sqrt(Math.pow(b.x - a.x, 2) + Math.pow(b.y - a.y, 2));
  }

  rotateCoord(coord: { x: number; y: number }, rotationAngle: number) {
    const angle = Math.atan2(coord.y, coord.x);
    const magnitude = this.euclideanDistance(coord, { x: 0, y: 0 });
    return {
      x: magnitude * Math.cos(angle + rotationAngle),
      y: magnitude * Math.sin(angle + rotationAngle),
    };
  }

  chordLength(radius: number, subtendedAngle: number) {
    return 2 * radius * Math.sin(subtendedAngle / 2);
  }

  rescale() {
    if (this.ref.current == null) {
      console.log("NULL");
      return;
    }

    const scale =
      Math.min(this.ref.current.clientWidth, this.ref.current.clientHeight) /
      this.props.pinnedRadius /
      2 /
      (1 + this.MARGIN);

    this.setState({
      scale: { x: scale, y: scale },
      offset: {
        x: this.ref.current.clientWidth / 2,
        y: this.ref.current.clientHeight / 2,
      },
    });
  }
  componentDidMount() {
    this.rescale();
    this.startTime = Date.now() / 1000;
    this.interval = setInterval(
      () => this.changeRotationAngle(),
      this.REFRESH_FREQUENCY
    );
  }
  changeRotationAngle() {
    let angle =
      (((Date.now() / 1000 - this.startTime) * this.props.rotationSpeed) %
        (2 * (this.props.maxAngle - this.props.minAngle))) -
      (this.props.maxAngle - this.props.minAngle);

    // Allow reversing of direction
    if (angle < 0) {
      angle = -angle;
    }
    this.setState({
      rotationAngle: angle,
    });
  }
  componentWillUnmount() {
    clearInterval(this.interval);
  }
}
export default IrisVisual;
