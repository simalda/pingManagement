import React from 'react';
import { Route } from "react-router-dom";
import history from "../JS/history";
import { Router } from "react-router";

import StartPage from "./StartPage";


class App extends React.Component {
  render() {
    return (
      <Router history={history}>
        <Route exact path="/" component={StartPage} />
      </Router>
    );
  }
}

export default App;
