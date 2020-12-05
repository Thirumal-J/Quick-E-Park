import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class NewRegistration extends Component {
	constructor(props) {
		super(props);

		this.state = {
			fullname: '',
			license_number:'',
			mobile_number:'',
			email: '',
			password: ''
		};

		this.update = this.update.bind(this);

		this.displayLogin = this.displayLogin.bind(this);
	}

	update(e) {
		let name = e.target.name;
		let value = e.target.value;
		this.setState({
			[name]: value
		});
	}

	displayLogin(e) {
		e.preventDefault();
		this.props.history.push({'pathname':'/vehicle_register',state:this.state});
	}

	render() {
		return (
			<div className="register">
				<div className="app_name">
          			<h1>QUICK-E-Park</h1>
        		</div>
				<form onSubmit={this.displayLogin}>
					<h2>Registration</h2>

					<div className="name">
						<input
							type="text"
							placeholder="Full Name"
							name="fullname"
							value={this.state.fullname}
							onChange={this.update}
						/>
					</div>

					<div className="license_number">
						<input
							type="text"
							placeholder="Driving license number"
							name="license_number"
							value={this.state.license_number}
							onChange={this.update}
						/>
					</div>

					<div className="mobile_number">
						<input
							type="text"
							placeholder="Mobile number"
							name="mobile_number"
							value={this.state.mobile_number}
							onChange={this.update}
						/>
					</div>

					<div className="email">
						<input
							type="text"
							placeholder="Email"
							name="email"
							value={this.state.email}
							onChange={this.update}
						/>
					</div>

					<div className="pasword">
						<input
							type="password"
							placeholder="Password"
							name="password"
							value={this.state.password}
							onChange={this.update}
						/>
					</div>

					<div className="password">
						<input type="password" placeholder="Confirm Password" name="password1" />
					</div>

					<input type="submit" value="Next" />
				</form>

				<div className="links">
					<Link to="/">Back to Login Page</Link>
				</div>
			</div>
		);
	}
}

export default NewRegistration;
