import React from "react";
import "../App.css";
import "../CSS/graph.css";
import Graph from "./Graph";
import Table from "./Table";
import Modal from "react-awesome-modal";
import momemt from "moment";
import * as moment from "moment";

const AllDateOption = "ALL";
const YearDateOption = "YEAR";
const MonthDateOption = "MONTH";
const DayDateOption = "DAY";
class StartPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      visibleModal: false,
      deleteResult: "",
      isLoadComplete: false,
      isError: false,
      data: [],
      charData: {},
      DateFilter: DayDateOption,
    };
  }

  componentDidMount() {
    this.updateData();
    var myVar = setInterval(()=>this.myTimer(), 60000);
  }

  updateData() {
    this.getChartData().then(
      (result) =>
        this.setState({
          ...this.state,
          isLoadComplete: true,
          visible: false,
          deleteResult: "",
          data: this.handleData(result["TableData"]),
          chartData: this.creatCompDatasets(result["GraphData"]),
        }),
      () => this.setState({ ...this.state, isError: true })
    );
  }

 myTimer() {
     console.log("Timer called")
     this.updateData()
  }

 

  getData() {
    return fetch(`http://127.0.0.1:5000/selectPings`, {}).then((response) =>
      response.json()
    );
  }

  getChartData() {
    return fetch(`http://127.0.0.1:5000/createChartData`, {}).then((response) =>
      response.json()
    );
  }

  deletePing(name) {
    var nameEncoded = encodeURIComponent(name);
    return fetch(
      `http://127.0.0.1:5000/delete/${nameEncoded}`
    ).then((response) => response.json());
  }

  creatCompDatasets(result) {
    let dataSets = [];
    let r = 0;
    let g = 0;
    let b = 0;
    result.forEach((item) => {
      r = this.creatNewRGB(r, g, b)[0];
      g = this.creatNewRGB(r, g, b)[1];
      b = this.creatNewRGB(r, g, b)[2];
      var dataForPing = [];
      item["pingTimeArrray"].forEach((item) => {
        console.log(item[1])
        dataForPing.push({
          x: moment(item[1]).local().toISOString(),
          y: item[0],
        });
      });
      dataSets.push({
        label: item["compName"],
        fill: false,
        lineTension: 0.5,
        backgroundColor: "rgba(75,192,192,1)",
        borderColor: "rgba(" + r + "," + g + "," + b + ",0.5)",
        borderWidth: 2,
        data: dataForPing,

        // data: item["pingArrray"],
      });
    });
    const scales = this.getScales();
    dataSets = this.chartData(scales, dataSets);

    return dataSets;
  }

  creatNewRGB(r, g, b) {
    r = r + 25;
    g = g + 50;
    b = b + 100;
    if (r + 25 > 256) {
      r = r % 256;
    } else if (g + 50 > 256) {
      g = g % 256;
    } else if (b + 100 > 256) {
      b = b % 256;
    }
    return [r, g, b];
  }

  chartData(scale, dataSets) {
    var options = {
      scales: scale,
      title: {
        display: true,
        text: "Ping live cycle",
        fontSize: 20,
      },
      legend: {
        display: true,
        position: "right",
      },
      maintainAspectRatio: false,
    };

    return {
      options: options,
      datasets: dataSets,
    };
  }

  dateButtonClicked(text) {
    this.setState({
      ...this.state,
      DateFilter: text,
    });
    this.updateData();
  }

  deleteItem(name) {
    this.deletePing(name).then(
      () => this.openModal("Succses"),
      () => this.openModal("Fail")
    );
  }

  getScales() {
    if (this.state.DateFilter === AllDateOption) {
      return {
        xAxes: [
          {
            type: "time",
            time: {
              parser: "YYYY-MM-DD HH:mm:ss",
              unit: "year",
              displayFormats: {
                day: "MM",
              },
              max: Date.now(),
            },
          },
        ],
      };
    }
    if (this.state.DateFilter === YearDateOption) {
      return {
        xAxes: [
          {
            type: "time",
            time: {
              parser: "YYYY-MM-DD HH:mm:ss",
              unit: "year",
              displayFormats: {
                day: "DD/MM",
              },
              min: moment().subtract(365, "days"),
              max: Date.now(),
            },
          },
        ],
      };
    } else if (this.state.DateFilter === MonthDateOption) {
      return {
        xAxes: [
          {
            type: "time",
            time: {
              parser: "YYYY-MM-DD HH:mm:ss",
              unit: "day",
              displayFormats: {
                day: "DD/MM",
              },
              min: moment().subtract(30, "days"),
              max: Date.now(),
            },
          },
        ],
      };
    } else if (this.state.DateFilter === DayDateOption) {
      return {
        xAxes: [
          {
            type: "time",
            time: {
              parser: "YYYY-MM-DD HH:mm:ss",
              unit: "hour",
              displayFormats: {
                day: "HH/mm",
              },
              min: moment().subtract(1, "days"),
              max: Date.now(),
            },
          },
        ],
      };
    }
  }

  handleData(result) {
    return result.map((item) => ({
      status: item["status"] === true ? "alive" : "dead",
      ping: item["ping"],
      name: item["name"],
      id: item["id"],
    }));
  }

  renderButtons() {
    const texts = ["ALL", "YEAR", "MONTH", "DAY"];
    const buttons = texts.map((text) => (
      <button
        key={text}
        className={
          this.state.DateFilter.toUpperCase() === text
            ? "buttonClicked"
            : "button"
        }
        onClick={() => this.dateButtonClicked(text)}
      >
        {text}
      </button>
    ));
    return <>{buttons}</>;
  }

  openModal(delRes) {
    this.setState({
      visible: true,
      deleteResult: delRes,
    });
  }

  closeModal() {
    this.updateData();
  }

  render() {
    if (this.state.isError) {
      return <div>Error</div>;
    } else if (!this.state.isLoadComplete) {
      return <div>Loading.....</div>;
    } else {
      return (
        <div>
          <Graph
            data={this.state.chartData}
            DateFilter={this.state.DateFilter}
          ></Graph>
          <div className="timeFrame">
            &nbsp;
            <span>TIME FRAME:</span>
            {this.renderButtons()}
          </div>
          <Table
            data={this.state.data}
            deleteItem={(id) => this.deleteItem(id)}
          ></Table>
          <Modal
            visible={this.state.visible}
            width="400"
            height="300"
            backgroundColor="beige"
            effect="fadeInUp"
            onClickAway={() => this.closeModal()}
          >
            <div>
              <h1>Delete report</h1>
              <p>{this.state.deleteResult}</p>
              <a href="javascript:void(0);" onClick={() => this.closeModal()}>
                Close
              </a>
            </div>
          </Modal>
        </div>
      );
    }
  }
}

export default StartPage;
