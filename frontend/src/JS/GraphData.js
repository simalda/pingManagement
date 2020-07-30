import moment from "moment";
import { datePeriod } from "./config";
import Point from "./Point";

class GraphData {
  constructor() {
    this.pingValue = 0; //#?!!!!
    this.time = 1;
  }

  createGraphData(dataFromServer, dateFilter) {
    var allPoints = this.createListOfAllPoints(dataFromServer);

    const startDate = this.getStartDate(dateFilter);
    const minDate = this.getMinTime(allPoints);
    const scales = this.getScales(dateFilter, allPoints, minDate);
    const dataSets = this.getDataSets(dataFromServer, startDate);
    const chartData = this.getChartData(scales, dataSets);

    return chartData;
  }

  createListOfAllPoints(dataFromServer) {
    let allPoints = [];
    dataFromServer.forEach((item) => {
      item["pingTimeArrray"].forEach((item) => {
        allPoints.push(
          new Point(moment(item[this.time]), item[this.pingValue])
        );
      });
    });
    return allPoints;
  }
  getChartData(scale, dataSets) {
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

  getDataSets(data, startDate) {
    let dataSets = [];
    data.forEach((item) => {
      var dataForPing = [];
      const pointsAfterStart = item["pingTimeArrray"].filter(
        (datum) => moment(datum.x) >= startDate
      );
      pointsAfterStart.forEach((item) => {
        dataForPing.push(
          new Point(moment(item[this.time]), item[this.pingValue])
        );
      });
      dataSets.push({
        label: item["name"],
        fill: false,
        lineTension: 0.5,
        backgroundColor: item["color"],
        borderColor: item["color"],
        borderWidth: 2,
        data: dataForPing,
      });
    });
    return dataSets;
  }

  getStartDate(dateFilter) {
    if (dateFilter === datePeriod.AllDateOption) {
      return moment().subtract(3650, "days");
    } //last 10 years
    else if (dateFilter === datePeriod.YearDateOption) {
      return moment().subtract(365, "days");
    } else if (dateFilter === datePeriod.MonthDateOption) {
      return moment().subtract(30, "days");
    } else if (dateFilter === datePeriod.DayDateOption) {
      return moment().subtract(1, "days");
    } else if (dateFilter === datePeriod.HourDateOption) {
      return moment().subtract(1, "hours");
    }
  }

  getScales(dateFilter, dataSets, minDate) {
    // const scaleMappings = [
    //   [
    //     datePeriod.AllDateOption,
    //     () => {
    //       xAxes: this.getXAxis("month", "MMM/YY", minDate);
    //     },
    //   ],
    //   [
    //     datePeriod.YearDateOption,
    //     () => {
    //       const startDate = moment().subtract(365, "days");
    //       return { xAxes: this.getXAxis("year", "DD/MM", startDate) };
    //     },
    //   ],
    // ];

    // const scales = new Map(scaleMappings);

    // return scales[dateFilter]();

    if (dateFilter === datePeriod.AllDateOption) {
      return { xAxes: this.getXAxis("month", "MMM/YY", minDate) };
    } else if (dateFilter === datePeriod.YearDateOption) {
      const startDate = moment().subtract(365, "days");
      return { xAxes: this.getXAxis("year", "DD/MM", startDate) };
    } else if (dateFilter === datePeriod.MonthDateOption) {
      const startDate = moment().subtract(30, "days");
      return this.scaleByDate("day", "DD/MM", startDate, dataSets);
    } else if (dateFilter === datePeriod.DayDateOption) {
      const startDate = moment().subtract(1, "days");
      return this.scaleByDate("hour", "HH", startDate, dataSets);
    } else if (dateFilter === datePeriod.HourDateOption) {
      const startDate = moment().subtract(1, "hours");
      return this.scaleByDate("minute", "mm", startDate, dataSets);
    }
  }

  scaleByDate(unit, day, startDay, dataSets) {
    return {
      xAxes: this.getXAxis(unit, day, startDay),
      yAxes: this.getYAxis(startDay, dataSets),
    };
  }
  getXAxis(unit, day, startDay) {
    return [
      {
        type: "time",
        time: {
          parser: "YYYY-MM-DD HH:mm:ss",
          unit: unit,
          // unitStepSize: 0.5,
          // round: 'hour',
          // tooltipFormat: "h:mm:ss a",
          displayFormats: {
            minute: "HH:mm",
            hour: "MMM D, h:mm",
            day: "MMM DD",
            month: "MMM DD",
            year: "MMM DD",
          },
          min: startDay,
          max: moment(Date.now()),
        },
      },
    ];
  }

  getYAxis(startDay, dataSets) {
    return [
      {
        display: true,
        ticks: {
          max: this.getMaxY(startDay, dataSets),
        },
      },
    ];
  }

  getMaxY(fromWhereToStartTime, allPoints) {
    const pointsAfterStart = allPoints.filter(
      (datum) => moment.parseZone(datum.x) >= fromWhereToStartTime
    );
    const yValues = pointsAfterStart.map((point) => point.y);
    const maxVal = Math.max(...yValues);
    return maxVal;
  }

  getMinTime(allPoints) {
    const xValues = allPoints.map((point) => point.x);
    const minVal = Math.min(...xValues);
    return minVal;
  }
}

export default GraphData;
