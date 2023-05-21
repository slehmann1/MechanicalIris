import React from "react";
import { BladeComponent, Blade } from "./Blade.tsx";
import ActuatorRing from "./ActuatorRing.tsx";
import { Geometry } from "./Geometry.ts";
import TabbedRing from "./TabbedRing.tsx";
import BasePlate from "./BasePlate.tsx";
import DiameterOutline from "./DiameterOutline.tsx";

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
    const chordLength = Geometry.chordLength(
      this.props.bladeRadius,
      this.props.subtendedAngle
    );

    for (let i = 0; i < this.props.numBlades; i++) {
      const bladeAngle = ((Math.PI * 2) / this.props.numBlades) * i;
      const theta_a =
        ((Math.PI * 2) / this.props.numBlades) * i + this.state.rotationAngle;
      const alpha = Math.acos(
        this.bound(
          (chordLength / this.props.pinnedRadius) *
            Math.cos(this.state.rotationAngle),
          -1,
          1
        )
      );
      let c = {
        x: 0,
        y: this.props.pinnedRadius,
      };
      c = Geometry.rotateAboutOrigin(c, bladeAngle);
      blades.push(
        new Blade(
          this.props.bladeRadius,
          this.props.subtendedAngle,
          theta_a,
          c,
          this.props.pinDiameter,
          this.props.bladeWidth,
          i,
          alpha
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
            <TabbedRing
              innerRadius={35}
              outerRadius={60}
              rotationAngle={-this.state.rotationAngle}
              tabWidth={10}
              tabHeight={10}
              offset={this.state.offset}
              scale={this.state.scale}
              colour={"red"}
            >
              {
                <ActuatorRing
                  pinCount={this.props.numBlades}
                  slotInnerRadius={34}
                  slotOuterRadius={42}
                  slotWidth={this.props.pinDiameter + this.props.clearance * 2}
                  rotationAngle={-this.state.rotationAngle}
                  offset={this.state.offset}
                  scale={this.state.scale}
                ></ActuatorRing>
              }
            </TabbedRing>

            <TabbedRing
              innerRadius={35}
              outerRadius={60}
              rotationAngle={0}
              tabWidth={10}
              tabHeight={10}
              offset={this.state.offset}
              scale={this.state.scale}
              colour={"green"}
            >
              {
                <BasePlate
                  pinCount={this.props.numBlades}
                  holeDiameter={this.props.pinDiameter}
                  pinnedRadius={this.props.pinnedRadius}
                  rotationAngle={0}
                  offset={this.state.offset}
                  scale={this.state.scale}
                ></BasePlate>
              }
            </TabbedRing>
            <DiameterOutline
              diameter={20}
              xPosition={80}
              offset={this.state.offset}
              scale={this.state.scale}
            ></DiameterOutline>

            <DiameterOutline
              diameter={60}
              xPosition={150}
              offset={this.state.offset}
              scale={this.state.scale}
            ></DiameterOutline>
          </g>
        </svg>
      </div>
    );
  }

  bound(num: number, min: number, max: number) {
    if (num < min) {
      return min;
    }
    if (num > max) {
      return max;
    }
    return num;
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
      (this.props.maxAngle - this.props.minAngle) +
      this.props.minAngle;

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
