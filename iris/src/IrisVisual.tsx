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
  MARGIN = 0.15;
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
    for (let i = 0; i < this.props.numBlades; i++) {
      const c = {
        x:
          this.props.pinnedRadius *
          Math.cos(((Math.PI * 2) / this.props.numBlades) * i),
        y:
          this.props.pinnedRadius *
          Math.sin(((Math.PI * 2) / this.props.numBlades) * i),
      };
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
          </g>
        </svg>
      </div>
    );
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
