import React from "react";
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
  const graphData = createGraphData(props);

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

function createGraphData(props) {
    var allPoints = [];
    props.data.forEach((item) => {
        item["pingTimeArrray"].forEach((item) => {
            allPoints.push({
            x: item[time],
            y: item[pingValue],
          });
        });})
  const startDate = getStartDate(props.DateFilter);
  const minDate = getMinTime(allPoints)
  const scales = getScales(props.DateFilter, allPoints, minDate);
  const dataSets = getDataSets(props.data, startDate);
  const chartData = getChartData(scales, dataSets);

  return chartData;
}


String.prototype.hashCode = function () {
  var hash = 0;
  if (this.length === 0) {
    return hash;
  }
  for (var i = 0; i < this.length; i++) {
    var char = this.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return hash;
};
function creatNewRGB(compName) {
  return [
    compName.hashCode() % 256,
    (compName.hashCode() + 50) % 256,
    (compName.hashCode() + 100) % 256,
  ];
}

function getChartData(scale, dataSets) {
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

function getDataSets(data, startDate) {
  let dataSets = [];
  data.forEach((item) => {
    let rVal = creatNewRGB(item["compName"])[r];
    let gVal = creatNewRGB(item["compName"])[g];
    let bVal = creatNewRGB(item["compName"])[b];
    var dataForPing = [];
    const pointsAfterStart = item["pingTimeArrray"].filter(
        (datum) => moment(datum.x) >= startDate
      );
      pointsAfterStart.forEach((item) => {
      dataForPing.push({
        x: moment(item[time]),
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
  return dataSets
}

function getStartDate(dateFilter) {
  if (dateFilter === datePeriod.AllDateOption) {
    return  moment().subtract(3650, "days");
  } //last 10 years
  else if (dateFilter === datePeriod.YearDateOption) {
    return  moment().subtract(365, "days");
  } else if (dateFilter === datePeriod.MonthDateOption) {
    return moment().subtract(30, "days");
  } else if (dateFilter === datePeriod.DayDateOption) {
    return  moment().subtract(1, "days");
  } else if (dateFilter === datePeriod.HourDateOption) {
    return  moment().subtract(1, "hours");
  }
}








function getScales(dateFilter, dataSets,minDate) {
  if (dateFilter === datePeriod.AllDateOption) {
    return { xAxes: getXAxis("month", "MMM/YY", minDate) };
  } else if (dateFilter === datePeriod.YearDateOption) {
    const startDate = moment().subtract(365, "days");
    return { xAxes: getXAxis("year", "DD/MM", startDate) };
  } else if (dateFilter === datePeriod.MonthDateOption) {
    const startDate = moment().subtract(30, "days");
    return scaleByDate("day", "DD/MM", startDate, dataSets);
  } else if (dateFilter === datePeriod.DayDateOption) {
    const startDate = moment().subtract(1, "days");
    return scaleByDate("hour", "HH/mm", startDate, dataSets);
  } else if (dateFilter === datePeriod.HourDateOption) {
    const startDate = moment().subtract(1, "hours");
    return scaleByDate("minute", "mm", startDate, dataSets);
  }
}

function scaleByDate(unit, day, startDay, dataSets) {
  return {
    xAxes: getXAxis(unit, day, startDay),
    yAxes: getYAxis(startDay, dataSets),
  };
}
function getXAxis(unit, day, startDay) {
  return [
    {
      type: "time",
      time: {
        parser: "YYYY-MM-DD HH:mm:ss",
        unit: unit,
        displayFormats: {
          day: day,
        },
        min: startDay,
        max: Date.now(),
      },
    },
  ];
}

function getYAxis(startDay, dataSets) {
  return [
    {
      display: true,
      ticks: {
        max: getMaxY(startDay, dataSets),
      },
    },
  ];
}

function getMaxY(fromWhereToStartTime, allPoints) {
    const pointsAfterStart = allPoints.filter(
      (datum) => moment.parseZone(datum.x) >= fromWhereToStartTime
    );
    const yValues = pointsAfterStart.map((point) => point.y);
    const maxVal = Math.max(...yValues);
    return maxVal;
    }

function getMinTime(allPoints){
    const xValues = allPoints.map((point) => point.x);
    const minVal = Math.min(...xValues);
    return minVal;
}
// function getMaxY(fromWhereToStartTime, dataSets) {
//   const mergedSeris = dataSets.map((dataset) => dataset.data).flat();
//   const pointsAfterStart = mergedSeris.filter(
//     (datum) => moment(datum.x) >= fromWhereToStartTime
//   );
//   const yValues = pointsAfterStart.map((point) => point.y);
//   const maxVal = Math.max(...yValues);
//   return maxVal;

  //     const valuesInTimeRange = []
  //     for (let i = 0; i < dataSets.length; i++){
  //         for(let j = 0; j < dataSets[i].data.length; j++){
  //             if ( dataSets[i].data[j]['x']  >= moment(fromWhereToStartTime).local().toISOString()) {
  //                 valuesInTimeRange.push(dataSets[i].data[j][pingValue])
  //             }
  //         }
  // }
  // return Math.max(valuesInTimeRange)


export default Graph;
