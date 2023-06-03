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
    bladeRadius: number;
    pinnedRadius: number;
    minAngle: number;
    maxAngle: number;
    speed: number;
  }
> {
  DEFAULT_BLADE_NUM = 10;
  DEFAULT_BLADE_WIDTH = 5;
  DEFAULT_MIN_DIAMETER = 10;
  DEFAULT_MAX_DIAMETER = 50;
  DEFAULT_PIN_DIAMETER = 3;
  DEFAULT_CLEARANCE = 0.5;
  DEFAULT_BLADE_RADIUS = 48;
  DEFAULT_PINNED_RADIUS = 50;
  DEFAULT_MIN_ANGLE = 4.596586633962879;
  DEFAULT_MAX_ANGLE = 5.0171595760221885;
  DEFAULT_ROTATIONAL_SPEED = 25;

  DXF_ZIP_FILENAME = "IrisDXFs.zip";

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
      bladeRadius: this.DEFAULT_BLADE_RADIUS,
      pinnedRadius: this.DEFAULT_PINNED_RADIUS,
      minAngle: this.DEFAULT_MIN_ANGLE,
      maxAngle: this.DEFAULT_MAX_ANGLE,
      speed: this.DEFAULT_ROTATIONAL_SPEED,
    };
    this.state = inputs;
    this.setState = this.setState.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.calculate = this.calculate.bind(this);
    this.downloadDXF = this.downloadDXF.bind(this);
    this.downloadBlob = this.downloadBlob.bind(this);
  }

  render() {
    return (
      <div>
        <Container>
          <form onSubmit={this.submitForm}>
            <Row>
              <Inputs
                numBlades={this.state.numBlades}
                bladeWidth={this.state.bladeWidth}
                minDiameter={this.state.minDiameter}
                maxDiameter={this.state.maxDiameter}
                pinDiameter={this.state.pinDiameter}
                clearance={this.state.clearance}
                speed={this.state.speed}
                callback={(property, value) => {
                  this.setState({
                    [property]: value,
                  });
                }}
              ></Inputs>
            </Row>
            <Row>
              <IrisVisual
                bladeRadius={this.state.bladeRadius}
                subtendedAngle={(Math.PI * 2) / 3}
                bladeWidth={this.state.bladeWidth}
                pinDiameter={this.state.pinDiameter}
                pinnedRadius={this.state.pinnedRadius}
                clearance={this.state.clearance}
                numBlades={this.state.numBlades}
                rotationSpeed={(this.state.speed * Math.PI) / 180}
                minAngle={this.state.minAngle}
                maxAngle={this.state.maxAngle}
                minApertureDiameter={this.state.minDiameter}
                maxApertureDiameter={this.state.maxDiameter}
              ></IrisVisual>
            </Row>
          </form>
          <Row>
            <button className="btn" onClick={this.downloadDXF}>
              Download DXF
            </button>
          </Row>
        </Container>
      </div>
    );
  }
  submitForm(e: any) {
    e.preventDefault();
    this.calculate();
  }
  getServerInputs() {
    return {
      bladeCount: this.state.numBlades,
      minDiameter: this.state.minDiameter,
      maxDiameter: this.state.maxDiameter,
      bladeWidth: this.state.bladeWidth,
      pinRadius: this.state.pinDiameter / 2,
      pinClearance: this.state.clearance,
    };
  }
  getQueryString(inputs: object) {
    /**
     * Creates a URL query string for an object where properties represent each element of the query
     */
    let str = "?";
    for (const input in inputs) {
      str += input + "=" + inputs[input] + "&";
    }
    str = str.substring(0, str.length - 1);
    return str;
  }
  downloadDXF() {
    const inputs = this.getServerInputs();
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const self = this;
    $.ajax({
      url:
        "http://127.0.0.1:8000/iris/dxf" +
        this.getQueryString(this.getServerInputs()),
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
      type: "GET",
      dataType: "text",
      mimeType: "text/plain; charset=x-user-defined",
      data: JSON.stringify(inputs),
      contentType: "application/json; charset=utf-8",
      processData: false,
      success: function (data) {
        console.log("DXF zips recieved successfully");
        let newContent = "";
        for (let i = 0; i < data.length; i++) {
          newContent += String.fromCharCode(data.charCodeAt(i) & 0xff);
        }
        const bytes = new Uint8Array(newContent.length);
        for (let i = 0; i < newContent.length; i++) {
          bytes[i] = newContent.charCodeAt(i);
        }
        const blob = new Blob([bytes], { type: "application/zip" });
        self.downloadBlob(blob, self.DXF_ZIP_FILENAME);
      },
    });
    return;
  }
  downloadBlob(blob: Blob, filename: string) {
    /**
     * Downloads the given blob as the filename
     */
    // Create an object URL for the blob object
    const url = URL.createObjectURL(blob);

    // Create a new anchor element
    const a = document.createElement("a");
    a.href = url;
    a.download = filename || "download";

    // Click handler that releases the object URL after the element has been clicked
    const clickHandler = () => {
      setTimeout(() => {
        URL.revokeObjectURL(url);
        removeEventListener("click", clickHandler);
      }, 150);
    };
    a.addEventListener("click", clickHandler, false);
    a.click();
  }
  calculate() {
    const inputs = this.getServerInputs();
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const app = this;
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
        app.setState({
          bladeRadius: data["blade_radius"],
          pinnedRadius: data["pinned_radius"],
          minAngle: data["min_angle"],
          maxAngle: data["max_angle"],
        });
        app.render();
        console.log(data["maxAngle"]);
      },
    });
  }

  setState(state) {
    super.setState(state);
    window.localStorage.setItem("Inputs", JSON.stringify(this.state));
  }
}

export default App;
