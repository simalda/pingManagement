import React from "react";
import "../App.css";
import "../CSS/graph.css";
import Graph from "./Graph";
import Table from "./Table";
import Modal from "react-awesome-modal";
import * as proxy from "../JS/proxy";
import {datePeriod} from "../JS/config"
 
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
      DateFilter: datePeriod.DayDateOption
    };
  }

  componentDidMount() {
    this.updateData();
    setInterval(()=>this.myTimer(), 60000);
  }

  updateData() {
    proxy.getChartData().then(
      (result) =>
        this.setState({
          ...this.state,
          isLoadComplete: true,
          visible: false,
          deleteResult: "",
          data:  result["TableData"],
          chartData: result["GraphData"],
        }),
      () => this.setState({ ...this.state, isError: true })
    );
  }

 myTimer() {
     console.log("Timer called")
     this.updateData()
  }
 
  dateButtonClicked(text) {
    this.setState({
      ...this.state,
      DateFilter: text,
    });
    this.updateData();
  }

  deleteItem(name) {
    proxy.deleteComp(name).then(
      () => this.openModal("Succses"),
      () => this.openModal("Fail")
    );
  }

  closeModal() {
    this.updateData();
  }

  openModal(delRes) {
    this.setState({
      visible: true,
      deleteResult: delRes,
    });
  }
  renderButtons() {
    const texts = [
      datePeriod.AllDateOption, 
      datePeriod.YearDateOption,
      datePeriod.MonthDateOption, 
      datePeriod.DayDateOption,
      datePeriod.HourDateOption
    ];
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
            width="300"
            height="200"            
            effect="fadeInUp"
            // onClickAway={() => this.closeModal()}
          >
            <div className='modal'>
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
