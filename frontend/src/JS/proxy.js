 

  export function getChartData() {
    return fetch(`http://127.0.0.1:5000/createChartData`, {}).then((response) =>
      response.json()
    );
  }

  export function deleteComp(name) {
    var nameEncoded = encodeURIComponent(name);
    return fetch(
      `http://127.0.0.1:5000/delete/${nameEncoded}`
    ).then((response) => response.json());
  }