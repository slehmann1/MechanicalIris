import "./App.css";
import React from "react";
import Inputs from "./Inputs.tsx";
import IrisVisual from "./IrisVisual.tsx";
import Cookies from "js-cookie";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import "bootstrap/dist/css/bootstrap.min.css";
import $ from "jquery";
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
    this.submitForm = this.submitForm.bind(this);
  }

  render() {
    return (
      <form onSubmit={this.submitForm}>
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
              bladeRadius={48}
              subtendedAngle={(Math.PI * 2) / 3}
              bladeWidth={this.state.bladeWidth}
              pinDiameter={this.state.pinDiameter}
              pinnedRadius={50}
              clearance={this.state.clearance}
              numBlades={this.state.numBlades}
              rotationSpeed={0.5}
              minAngle={4.596586633962879}
              maxAngle={5.0171595760221885}
            ></IrisVisual>
          </Row>
          <Row>
            <button className="btn"> Download DXF </button>
          </Row>
        </Container>
      </form>
    );
  }
  submitForm(e: any) {
    e.preventDefault();
    this.calculate();
  }
  calculate() {
    const inputs = { test: "HELLO" };
    $.ajax({
      url: "http://127.0.0.1:8000/iris",
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
      type: "POST",
      data: JSON.stringify(inputs),
      contentType: "application/json; charset=utf-8",
      processData: false,
      success: function (data) {
        console.log("Calculation completed successfully");
        console.log(data);
      },
    });
  }

  setState(state) {
    super.setState(state);
    window.localStorage.setItem("Inputs", JSON.stringify(this.state));
  }
}

export default App;
