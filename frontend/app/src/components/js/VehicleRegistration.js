import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class VehicleRegister extends Component {
	constructor(props) {
		super(props);
		this.state = {
			Vehicle_Number: '',
		};

		this.update = this.update.bind(this);

		this.displayLogin = this.displayLogin.bind(this);
	}

	update(e) {
		let name = e.target.name;
		let value = e.target.value;
		this.setState({[name]: value
		});
	}

	displayLogin(e) {
		e.preventDefault();
		console.log('You have successfully registered');
		console.log(this.props.location.state);
		console.log(this.state)
	}

	render() {
		return (
			<div className="vehicle_register">
				<form onSubmit={this.displayLogin}>
					<h2>Vehicle Registration</h2>

					<div className="Vehicle_Number">
						<input
							type="text"
							placeholder="Vehicle Number"
							name="Vehicle_Number"
							value={this.state.Vehicle_Number}
							onChange={this.update}
						/>
					</div>

					<input type="submit" value="Register" />
				</form>
				<div className="links">
					<Link to="/dashboard">Skip</Link>
				</div>
				<div className="links">
					<Link to="/new_registration">Back to Previous Page</Link>
				</div>
				<div className="links">
					<Link to="/">Back to Login Page</Link>
				</div>
				
			</div>
		);
	}
}

export default VehicleRegister;
