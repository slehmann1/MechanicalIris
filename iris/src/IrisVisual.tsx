import React from "react";
import { BladeComponent, Blade } from "./Blade.tsx";
import ActuatorRing from "./ActuatorRing.tsx";
import { Geometry } from "./Geometry.ts";
import TabbedRing from "./TabbedRing.tsx";
import BasePlate from "./BasePlate.tsx";
import DiameterOutline from "./DiameterOutline.tsx";
import AngularDimension from "./AngularDimension.tsx";

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
    minApertureDiameter: number;
    maxApertureDiameter: number;
  },
  {
    height: number;
    width: number;
    offset: { x: number; y: number };
    scale: { x: number; y: number };
    rotationAngle: number;
  }
> {
  MARGIN = 1;
  REFRESH_FREQUENCY = 15;
  TAB_SIZE = 10;
  DIMENSION_MARGIN = 0.25;
  ACTUATOR_RING_COLOUR = "#282c34";
  BASE_PLATE_COLOUR = "#282c34";

  ref?: any;
  interval: any;
  startTime: number;
  constructor(props: any) {
    super(props);
    this.ref = React.createRef();
    this.state = {
      height: 1,
      width: 1,
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

    const newScale =
      this.state.height /
      (this.props.pinnedRadius +
        this.props.pinDiameter +
        this.props.bladeWidth / 2 +
        this.TAB_SIZE) /
      (2 + this.MARGIN);
    // Check if props have changed scale
    if (this.state.height != 1 && this.state.scale.x != newScale) {
      this.rescale();
    }

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

            <TabbedRing
              innerRadius={
                this.props.maxApertureDiameter / 2 + this.props.clearance * 2
              }
              outerRadius={
                this.props.pinnedRadius +
                this.props.pinDiameter +
                this.props.bladeWidth / 2
              }
              rotationAngle={-this.state.rotationAngle}
              tabWidth={this.TAB_SIZE}
              tabHeight={this.TAB_SIZE}
              offset={this.state.offset}
              scale={this.state.scale}
              colour={ActuatorRing.COLOUR}
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
              innerRadius={
                (this.props.maxApertureDiameter / 2 +
                  this.props.clearance * 2) *
                1.02
              }
              outerRadius={
                (this.props.pinnedRadius +
                  this.props.pinDiameter +
                  this.props.bladeWidth / 2) *
                1.02
              }
              rotationAngle={0}
              tabWidth={this.TAB_SIZE}
              tabHeight={this.TAB_SIZE}
              offset={this.state.offset}
              scale={this.state.scale}
              colour={BasePlate.COLOUR}
            >
              {
                <BasePlate
                  pinCount={this.props.numBlades}
                  holeDiameter={this.props.pinDiameter + this.props.clearance}
                  pinnedRadius={this.props.pinnedRadius}
                  rotationAngle={0}
                  offset={this.state.offset}
                  scale={this.state.scale}
                ></BasePlate>
              }
            </TabbedRing>

            <DiameterOutline
              diameter={this.props.minApertureDiameter}
              xPosition={
                (this.props.pinnedRadius +
                  this.props.pinDiameter +
                  this.props.bladeWidth / 2 +
                  this.TAB_SIZE) *
                (1 + this.DIMENSION_MARGIN)
              }
              offset={this.state.offset}
              scale={this.state.scale}
            ></DiameterOutline>
            <DiameterOutline
              diameter={this.props.maxApertureDiameter}
              xPosition={
                (this.props.pinnedRadius +
                  this.props.pinDiameter +
                  this.props.bladeWidth / 2 +
                  this.TAB_SIZE) *
                Math.pow(1 + this.DIMENSION_MARGIN, 3)
              }
              offset={this.state.offset}
              scale={this.state.scale}
            ></DiameterOutline>
            <AngularDimension
              startAngle={this.props.minAngle}
              endAngle={this.props.maxAngle}
              radialDiameter={
                this.props.pinnedRadius +
                this.props.pinDiameter +
                this.props.bladeWidth / 2
              }
              dimensionRadialPosition={
                (this.props.pinnedRadius +
                  this.props.pinDiameter +
                  this.props.bladeWidth / 2 +
                  this.TAB_SIZE) *
                (1 + this.DIMENSION_MARGIN)
              }
              offset={this.state.offset}
              scale={this.state.scale}
            ></AngularDimension>
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
    console.log(this.ref.current.clientHeight);
    const scale =
      Math.min(this.ref.current.clientWidth, this.ref.current.clientHeight) /
      (this.props.pinnedRadius +
        this.props.pinDiameter +
        this.props.bladeWidth / 2 +
        this.TAB_SIZE) /
      (2 + this.MARGIN);

    this.setState({
      height: this.ref.current.clientHeight,
      width: this.ref.current.clientWidth,
      scale: { x: scale, y: scale },
      offset: {
        x: this.ref.current.clientWidth / 2,
        y: this.ref.current.clientHeight / 2 - this.TAB_SIZE,
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
    if (angle < this.props.minAngle) {
      angle = this.props.minAngle - (angle - this.props.minAngle);
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
