import React, { Component } from 'react'
import { Bar, Line, Pie } from 'react-chartjs-2'
import ReactTable from 'react-table-6'
// import SimpleTable from 'react-simple-table'
import '../CSS/table.css'
import del from '../delete.png'
class Table extends Component {
    constructor(props) {
        super(props)
        this.state = {
            test: 'delete',
            
            }
        }

        getColumns(){
            return [{
                Header: () => (
                    <span>
                        <i className="fa-tasks" /> Delete
                    </span>
                ),
                accessor: 'delete',
                width: 150,

                Cell: props => { return <img className='image' src={del} alt={"Delete"} h={( index)=>this.deleteItem( index)} /> }
            }
                , {
                Header: () => (
                    <span>
                        <i className="fa-tasks" /> Status
                    </span>
                ),
                accessor: 'status',
                align: "center",
            }, {
                id: 'Ping', // Required because our accessor is not a string
                Header: 'Ping',
                accessor: d => d.ping // Custom value accessors!
            }, {
                Header: props => <span>Name</span>, // Custom header components!
                accessor: 'name',
                align: "center",
            }]
        }
    
    deleteItem(index) {
        delete this.props.data[index]
        this.setState({
            ...this.state,
            data: this.props.data,
        test: "Sofa"

        });
    }
    render() {
        let tes  
        if (this.state.test==="Sofa"){
tes =   (
<div>"Sofa"</div>
)
 
        }
        return <div className='table'>
            {tes}
            <ReactTable
            data={this.props.data}
            columns={this.getColumns()}
            showPagination={false}
            defaultPageSize={this.props.data.length}
            getTrProps={(state, rowInfo, column) => {
                return {
                    style: {
                        background: rowInfo.row.status === 'alive' ? '#bbcfb2' : '#cfbab2'
                    },
                    onClick: (e, handleOriginal) => {
                        console.log("A Td Element was clicked!");
                        console.log("It was in this row:", rowInfo);

                        // IMPORTANT! React-Table uses onClick internally to trigger
                        // events like expanding SubComponents and pivots.
                        // By default a custom 'onClick' handler will override this functionality.
                        // If you want to fire the original onClick handler, call the
                        // 'handleOriginal' function.
                        if (handleOriginal) {
                           handleOriginal();
                        }
                    }
                }
            }}
            getTdProps={(state, rowInfo, column, instance) => {
                return {
                  onClick: (e, handleOriginal) => {
                    console.log("A Td Element was clicked!");
                    console.log("it produced this event:", e);
                    console.log("It was in this column:", column);
                    console.log("It was in this row:", rowInfo);
                    console.log("It was in this table instance:", instance);
                    if(column.id === "delete")(
                        this.deleteItem(rowInfo.index)
                    )
                    // IMPORTANT! React-Table uses onClick internally to trigger
                    // events like expanding SubComponents and pivots.
                    // By default a custom 'onClick' handler will override this functionality.
                    // If you want to fire the original onClick handler, call the
                    // 'handleOriginal' function.
                    if (handleOriginal) {
                      handleOriginal();
                    }
                  }}}}
        />
        

        </div>
    }
}

export default Table 