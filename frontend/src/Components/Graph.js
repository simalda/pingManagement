import React  from "react";
import { Line } from "react-chartjs-2";
import "../CSS/graph.css";
import * as moment from "moment";
import { datePeriod } from "../JS/config";

const r = 0;
const g = 1;
const b = 2;
const pingValue = 0;
var time = 1; 

function Graph(props) {
  const graphData = creatCompDatasets(props);
 

  return (
    <div className="lineChart">
      <Line
        data={graphData}
        height={400}
        width={600}
        options={graphData.options}
      />
    </div>
  );
}

function creatCompDatasets(props) {
  let dataSets = [];
  props.data.forEach((item) => {
    let rVal = creatNewRGB(item["compName"])[r];
    let gVal = creatNewRGB(item["compName"])[g];
    let bVal = creatNewRGB(item["compName"])[b];
    var dataForPing = [];
    item["pingTimeArrray"].forEach((item) => {
      dataForPing.push({
        x: moment(item[time]).local().toISOString(),
        y: item[pingValue],
      });
    });
    dataSets.push({
      label: item["compName"],
      fill: false,
      lineTension: 0.5,
      backgroundColor: "rgba(75,192,192,1)",
      borderColor: "rgba(" + rVal + "," + gVal + "," + bVal + ",0.5)",
      borderWidth: 2,
      data: dataForPing,
    });
  });
  const scales = getScales(props.DateFilter);
  dataSets = chartData(scales, dataSets);

  return dataSets;
}
String.prototype.hashCode = function() {
    var hash = 0;
    if (this.length === 0) {
        return hash;
    }
    for (var i = 0; i < this.length; i++) {
        var char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}
function creatNewRGB(compName) {
//   r = compName.hashCode();
//   g = compName.hashCode() + 50;
//   b = compName.hashCode() + 100;
//   if (r + 25 > 256) {
//     r = r % 256;
//   } else if (g + 50 > 256) {
//     g = g % 256;
//   } else if (b + 100 > 256) {
//     b = b % 256;
//   }
  return [compName.hashCode()%256, (compName.hashCode() + 50)%256, (compName.hashCode() + 100)%256];
}

function chartData(scale, dataSets) {
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

function getScales(dateFilter) {
  if (dateFilter === datePeriod.AllDateOption) {
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
  } else if (dateFilter === datePeriod.YearDateOption) {
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
  } else if (dateFilter === datePeriod.MonthDateOption) {
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
  } else if (dateFilter === datePeriod.DayDateOption) {
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
  } else if (dateFilter === datePeriod.HourDateOption) {
    return {
      xAxes: [
        {
          type: "time",
          time: {
            parser: "YYYY-MM-DD HH:mm:ss",
            unit: "minute",
            displayFormats: {
              day: "mm",
            },
            min: moment().subtract(1, "hours"),
            max: Date.now(),
          },
        },
      ],
    };
  }
}

export default Graph;
