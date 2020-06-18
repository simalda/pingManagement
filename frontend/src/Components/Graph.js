import React, { Component } from 'react'
import {Line} from 'react-chartjs-2'
import '../CSS/graph.css'

class Graph extends Component {
    constructor(props) {
        super(props)
        // this.convertFromData()
        this.state = {
            labels: this.getLabels(),
            datasets: [
                {
                    label: 'comp1',
                    fill: false,
                    lineTension: 0.5,
                    backgroundColor: 'rgba(75,192,192,1)',
                    borderColor: 'blue',
                    borderWidth: 2,
                    data: [65, 59, 80, 81, 56]
                }
            ]
        }
    }
    getLabels(){
    if (this.props.DateFilter==='Month'){
        return ['January', 'February', 'March',
        'April', 'May']
    }
    }
    render() {
        return (
            <div className = 'lineChart'>
                <Line
                    data={this.state}
                    height={400}
                    width={600}
                    options={{
                        title: {
                            display: true,
                            text: 'Ping live cycle',
                            fontSize: 20
                        },
                        legend: {
                            display: true,
                            position: 'right'
                        },
                     maintainAspectRatio: false 
                    }}
                />
                <div className='timeFrame'> TIME FRAME: <button className="button ">ALL</button><button className="button  ">YEAR</button><button className="button">MONTH</button><button className="button">DAY</button>  </div>
            </div>
        )
    }
}

export default Graph 