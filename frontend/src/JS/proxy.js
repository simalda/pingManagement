export function getChartData() {
  return fetch(`http://127.0.0.1:5000/createChartData`, {}).then((response) => {
    if (!response.ok) {
      throw response;
    }
    return response.json();
  });
}

export function deleteComp(name) {
  var nameEncoded = encodeURIComponent(name);
  return fetch(`http://127.0.0.1:5000/delete/${nameEncoded}`).then(
    (response) => {
      if (!response.ok) {
        throw response;
      }
      return response.json();
    }
  );
}

// export function getChartData() {
//   return fetch(`http://127.0.0.1:5000/createChartData`, {}).then(
//     (response) => {
//       // console.log(response);
//       if (!response.ok) {
//         console.log("Status Code: " + response.status);
//         return FetchResult.CreateBad(response.status)
//       }
//       return response.json().then(json=>FetchResult.CreateGood(json));
//     },
//     error=> FetchResult.CreateBad(error.toString())
//   );
// }
export class FetchResult {
  constructor(isGood, error, value) {
    this.isGood = isGood;
    this.error = error;
    this.value = value;
  }
  static CreateGood(value) {
    return new FetchResult(true, null, value);
  }
  static CreateBad(error) {
    return new FetchResult(false, error, null);
  }
}
