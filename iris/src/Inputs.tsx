import React from "react";
import parse from "html-react-parser";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";

class Inputs extends React.Component<{
  numBlades: number;
  bladeWidth: number;
  minDiameter: number;
  maxDiameter: number;
  pinDiameter: number;
  clearance: number;
  speed: number;
  callback: (string, number) => void;
}> {
  constructor(props: any) {
    super(props);
  }

  render() {
    return (
      <Container className="inputs">
        <Row>
          <Col>
            <InputGroup
              text="Number Of Blades"
              value={this.props.numBlades}
              changeCallback={(value: number) => {
                this.props.callback("numBlades", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
          <Col>
            <InputGroup
              text="Blade Width (mm)"
              value={this.props.bladeWidth}
              changeCallback={(value: number) => {
                this.props.callback("bladeWidth", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
        </Row>
        <Row>
          <Col>
            <InputGroup
              text="Minimum Aperture Diameter (mm)"
              value={this.props.minDiameter}
              changeCallback={(value: number) => {
                this.props.callback("minDiameter", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
          <Col>
            <InputGroup
              text="Maximum Aperture Diameter (mm)"
              value={this.props.maxDiameter}
              changeCallback={(value: number) => {
                this.props.callback("maxDiameter", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
        </Row>
        <Row>
          <Col>
            <InputGroup
              text="Pin Diameter (mm)"
              value={this.props.pinDiameter}
              changeCallback={(value: number) => {
                this.props.callback("pinDiameter", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
          <Col>
            <InputGroup
              text="Pin Clearance (mm)"
              value={this.props.clearance}
              changeCallback={(value: number) => {
                this.props.callback("clearance", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
        </Row>
        <Row>
          <Col>
            <InputGroup
              text="Rotational Speed (°/s)"
              value={this.props.speed}
              changeCallback={(value: number) => {
                this.props.callback("speed", value);
              }}
              wide={false}
            ></InputGroup>
          </Col>
          <Col>
            <button className="btn"> Calculate </button>
          </Col>
        </Row>
      </Container>
    );
  }
}

class InputGroup extends React.Component<{
  wide: boolean;
  text: string;
  value: number;
  changeCallback: (_: number) => void;
}> {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="input-group">
        <div className="input-group-text">{parse(this.props.text)}</div>
        <input
          className="form-control"
          type="number"
          min="0"
          step="0.001"
          value={this.props.value || 0}
          onChange={(evt) =>
            this.props.changeCallback(Number(evt.target.value))
          }
        />
      </div>
    );
  }
}

export default Inputs;
