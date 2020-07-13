import React from "react";
import { Line } from "react-chartjs-2";
import "../CSS/graph.css";

 


function Graph(props) {
  // const graphData = GraphData.createGraphData(props);

  return (
    <div className="lineChart">
      <Line
        data={props.data}
        height={400}
        width={600}
        options={props.data.options}
      />
    </div>
  );
}


export default Graph;
