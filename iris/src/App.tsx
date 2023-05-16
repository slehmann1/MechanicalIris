import "./App.css";
import React from "react";
import Inputs from "./Inputs.tsx";
import IrisVisual from "./IrisVisual.tsx";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import "bootstrap/dist/css/bootstrap.min.css";

class App extends React.Component<
  null,
  {
    numBlades: number;
    bladeWidth: number;
    minDiameter: number;
    maxDiameter: number;
    pinDiameter: number;
    clearance: number;
  }
> {
  DEFAULT_BLADE_NUM = 10;
  DEFAULT_BLADE_WIDTH = 5;
  DEFAULT_MIN_DIAMETER = 10;
  DEFAULT_MAX_DIAMETER = 50;
  DEFAULT_PIN_DIAMETER = 3;
  DEFAULT_CLEARANCE = 0.5;

  constructor(props) {
    super(props);
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    const inputs = JSON.parse(window.localStorage.getItem("Inputs")) || {
      numBlades: this.DEFAULT_BLADE_NUM,
      bladeWidth: this.DEFAULT_BLADE_WIDTH,
      minDiameter: this.DEFAULT_MIN_DIAMETER,
      maxDiameter: this.DEFAULT_MAX_DIAMETER,
      pinDiameter: this.DEFAULT_PIN_DIAMETER,
      clearance: this.DEFAULT_CLEARANCE,
    };
    this.state = inputs;
    this.setState = this.setState.bind(this);
  }

  render() {
    return (
      <div className="App">
        <Container>
          <Row>
            <Inputs
              numBlades={this.state.numBlades}
              bladeWidth={this.state.bladeWidth}
              minDiameter={this.state.minDiameter}
              maxDiameter={this.state.maxDiameter}
              pinDiameter={this.state.pinDiameter}
              clearance={this.state.clearance}
              callback={(property, value) => {
                this.setState({
                  [property]: value,
                });
              }}
            ></Inputs>
          </Row>
          <Row>
            <IrisVisual
              bladeRadius={10}
              subtendedAngle={(Math.PI * 2) / 3}
              bladeWidth={this.state.bladeWidth}
              pinDiameter={this.state.pinDiameter}
              pinnedRadius={20}
              clearance={this.state.clearance}
              numBlades={this.state.numBlades}
            ></IrisVisual>
          </Row>
        </Container>
      </div>
    );
  }
  setState(state) {
    super.setState(state);
    window.localStorage.setItem("Inputs", JSON.stringify(this.state));
  }
}

export default App;
