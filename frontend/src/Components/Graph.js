import React, { Component } from 'react'
import {Line} from 'react-chartjs-2'
import '../CSS/graph.css'

class Graph extends Component {
    constructor(props) {
        super(props)
        // this.convertFromData()
        this.state = {
             
            
        }}
        
    
   
    render() {
        
        return (
            <div className = 'lineChart'>
                <Line
                    data={this.props.data}
                    height={400}
                    width={600}
                    options={this.props.data.options}
                />
               
            </div>
        )
    }
}

export default Graph 