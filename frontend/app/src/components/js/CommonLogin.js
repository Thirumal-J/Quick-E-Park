import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class CommonLogin extends Component {
	// constructor(props) {
	// 	super(props);

	// 	this.state = {
	// 		fullname: '',
	// 		license_number:'',
	// 		mobile_number:'',
	// 		email: '',
	// 		password: ''
	// 	};

	// 	this.update = this.update.bind(this);

	// 	this.displayLogin = this.displayLogin.bind(this);
	// }

	// update(e) {
	// 	let name = e.target.name;
	// 	let value = e.target.value;
	// 	this.setState({
	// 		[name]: value
	// 	});
	// }

	// displayLogin(e) {
	// 	e.preventDefault();
	// 	this.props.history.push({'pathname':'/vehicle_register',state:this.state});
	// }

	render() {
		return (
			<div className="register">
				<div className="app_name">
          			<h1>QUICK-E-Park</h1>
        		</div>
			</div>
		);
	}
}

export default CommonLogin;
