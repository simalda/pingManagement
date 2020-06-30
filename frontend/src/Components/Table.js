import React, { Component } from "react";
import ReactTable from "react-table-6";
import "../CSS/table.css";
import del from "../delete.png";
class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
  }
//   componentDidMount() {
//     this.setState({
//       ...this.state,
//       data: this.handleData(),
//     });
//   }
  getColumns() {
    return [
      {
        Header: () => (
          <span>
            <i className="fa-tasks" /> Delete
          </span>
        ),
        accessor: "delete",
        width: 150,

        Cell: (props) => {
          return <img className="image" src={del} alt={"Delete"} />;
        },
      },
      {
        Header: () => (
          <span>
            <i className="fa-tasks" /> Status
          </span>
        ),
        accessor: "status",
        align: "center",
      },
      {
        id: "Ping", // Required because our accessor is not a string
        Header: "Ping",
        accessor: (d) => d.ping, // Custom value accessors!
      },
      {
        Header: (props) => <span>Name</span>, // Custom header components!
        accessor: "name",
        align: "center",
      },
    ];
  }

  handleData() {
    return this.props.data.map((item) => ({
      status: item["status"],
      ping: item["ping"],
      name: item["name"],
      id: item["id"],
    }));
  }

  render() {
    const tableData =this.handleData();
    return (
      <div className="table">
        <ReactTable
          data={tableData}
          columns={this.getColumns()}
          showPagination={false}
          pageSize={this.props.data.length}
          getTrProps={(state, rowInfo, column) => {
            if (!rowInfo) {
              return false;
            }
            return {
              style: {
                background:
                  rowInfo.row.status === "alive" ? "#bbcfb2" : "#cfbab2",
              },
              onClick: (e, handleOriginal) => {
                if (handleOriginal) {
                  handleOriginal();
                }
              },
            };
          }}
          getTdProps={(state, rowInfo, column, instance) => {
            return {
              onClick: (e, handleOriginal) => {
                console.log("It was in this column:", column);
                console.log("It was in this row:", rowInfo);
                if (column.id === "delete")
                  this.props.deleteItem(rowInfo.original.name);
                if (handleOriginal) {
                  handleOriginal();
                }
              },
            };
          }}
        />
      </div>
    );
  }
}

export default Table;
