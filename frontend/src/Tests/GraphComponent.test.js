import moment from "moment";
import { datePeriod } from "../JS/config";
import GraphData from "../JS/GraphData";
import Point from "../JS/Point";

describe("Graph Page", () => {
  let DateFilter = "DAY";
  const data = [
    {
      name: "DESKTOP-SOFA-TEST",
      color: "rgba(11,99,81,0.5)",
      pingTimeArrray: [
        [186, "Mon, 13 Jul 2020 14:43:56 GMT"],
        [187, "Mon, 13 Jul 2020 14:53:57 GMT"],
        [165, "Mon, 13 Jul 2020 15:03:59 GMT"],
        [180, "Mon, 13 Jul 2020 15:14:00 GMT"],
      ],
    },
    {
      name: "DESKTOP-ADAM-TEST",
      color: "rgba(194,253,65,0.5)",
      pingTimeArrray: [
        [243, "Mon, 13 Jul 2020 12:27:36 GMT"],
        [179, "Mon, 13 Jul 2020 12:37:37 GMT"],
        [201, "Mon, 13 Jul 2020 12:47:39 GMT"],
        [109, "Mon, 13 Jul 2020 12:57:40 GMT"],
        [161, "Mon, 13 Jul 2020 13:07:41 GMT"],
        [180, "Mon, 13 Jul 2020 13:17:42 GMT"],
      ],
    },
  ];
  beforeEach(() => {});

  afterEach(async () => {});

  test("Check that createListOfAllPoints have correct number of points in list ", () => {
    const gd = new GraphData();
    let allPoints = gd.createListOfAllPoints(data);
    expect(allPoints.length).toEqual(10);
  });

  test("Check that createListOfAllPoints actially contains points from different comps in the  list- first comp", () => {
    const gd = new GraphData();
    let allPoints = gd.createListOfAllPoints(data);
    expect(allPoints[0].y).toEqual(186);
  });

  test("Check that createListOfAllPoints actially contains points from different comps in the  list - second comp", () => {
    const gd = new GraphData();
    let allPoints = gd.createListOfAllPoints(data);
    expect(allPoints[4].y).toEqual(243);
  });
 
  test("Check that getMinTime bring the least time value", () => {
    const gd = new GraphData();
    let allPoints = gd.createListOfAllPoints(data);
    let minVal = gd.getMinTime(allPoints)
    expect(minVal).toEqual(1594643256000);
  });

test("Check that getMaxY bring the max ping value", () => {
    const gd = new GraphData();
    let allPoints = gd.createListOfAllPoints(data);
    const maxYValue = gd.getMaxY(moment("Mon, 6 Jul 2020 12:27:36 GMT"), allPoints)
    expect(maxYValue).toEqual(243);
  });

 
  test("Check getDataSets have correct comp name on first place", () => {
    const gd = new GraphData();
    let dataSets = gd.getDataSets(data, moment("Mon, 6 Jul 2020 12:27:36 GMT"));
    expect(dataSets[0]['label']).toEqual("DESKTOP-SOFA-TEST");
  });

  test("Check getDataSets have correct color name on first place", () => {
    const gd = new GraphData();
    let dataSets = gd.getDataSets(data, moment("Mon, 6 Jul 2020 12:27:36 GMT"));
    expect(dataSets[0]['borderColor']).toEqual("rgba(11,99,81,0.5)");
  });

  test("Check that getStartDAy bring 24 hours back on 'DAY' filter", () => {
    const gd = new GraphData();
    let res = gd.getStartDate(DateFilter);
    expect(moment().subtract(1, "days")-res < 5).toBeTruthy();
  });

  test("Check that getStartDAy bring least date  for'ALL' filter ", () => {
    const gd = new GraphData();
    let res = gd.getStartDate('ALL');
    expect(res).toEqual(moment("Mon, 13 Jul 2020 12:27:36 GMT"));
  });
});
