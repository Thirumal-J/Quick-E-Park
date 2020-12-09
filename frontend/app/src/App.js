import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Login from './components/js/Login';
import NewRegistration from './components/js/NewRegistration';
import VehicleRegistration from './components/js/VehicleRegistration';
import CommonLogin from './components/js/CommonLogin';
// import Dashboard from './components/js/SignInSide';

import './App.css';

class App extends Component {
  render() {
    return (
      <div className="container">
        <Route exact path="/" component={Login} />
        <Route exact path="/2" component={Login} />
        <Route exact path="/loginpage" component={CommonLogin}/>
        <Route path="/new_registration" component={NewRegistration} />
        <Route path="/vehicle_register" component={VehicleRegistration}/>
        {/* <Route path="/vehicle_register" component={VehicleRegistration}/> */}
        {/* <Route path="/dashboard" component={Dashboard}/> */}
      </div>
    );
  }
}

export default App;
