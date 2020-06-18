import React from "react";
import "../App.css";
import Graph from "./Graph";
import Table from "./Table";

class StartPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoadComplete: false,
      isError: false,
      data: [],
    };
  }
  componentDidMount() {
    this.getData().then(
      (result) =>
        this.setState({
          ...this.state,
          isLoadComplete: true,
          data: this.handleData(result),
        }),
      () => this.setState({ ...this.state, isError: true })
    );
  } 

  //     {
  //         status: 'alive',
  //         ping: '123',
  //         name: 'Tanner Linsley',
  //     }, {
  //         status: 'alive',
  //         ping: '123',
  //         name: 'Tanner Linsley',
  //     }, {
  //         status: 'met',
  //         ping: '123',
  //         name: 'Tanner Linsley',
  //     }, {
  //         status: 'alive',
  //         ping: '123',
  //         name: 'Tanner Linsley',
  //     }, {
  //         status: 'met',
  //         ping: '123',
  //         name: 'Tanner Linsley',
  //     }, {
  //         status: 'alive',
  //         ping: '444',
  //         name: 'Sofa',
  //     }, {
  //         status: 'alive',
  //         ping: '555',
  //         name: 'Supe Ping',
  //     }]

  getData() {
    return fetch(`http://127.0.0.1:5000/selectPings`, {}).then((response) =>
      response.json()
    );
  }

  handleData(result) {
    return result.map((item) => ({
      status: "alive",
      ping: item[2],
      name: item[1],
    }));
  }

  render() {
    if (this.state.isError) {
      return <div>Error</div>;
    } else if (!this.state.isLoadComplete) {
      return <div>Loading.....</div>;
    } else {
      return (
        <div>
          <Graph data={this.state.data}></Graph>
          <Table data={this.state.data}></Table>
        </div>
      );
    }
  }
}

export default StartPage;
