import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Login extends Component {
	constructor(props) {
		super(props);

		this.state = {
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
		console.log('You are logged in');
		console.log(this.state);
		this.setState({
			email: '',
			password: ''
		});
	}

	render() {
		return (
			<div className="login">
				<div className="app_name">
          			<h1>QUICK-E-Park</h1>
        		</div>
				<form onSubmit={this.displayLogin}>
					<h2>Login</h2>
					<div className="email">
						<input
							type="text"
							placeholder="Email"
							value={this.state.email}
							onChange={this.update}
							name="email"
						/>
					</div>

					<div className="password">
						<input
							type="password"
							placeholder="Password"
							value={this.state.password}
							onChange={this.update}
							name="password"
						/>
					</div>
					<div className="submit">
						<input type="submit" value="Login" />
					</div>
				</form>
				
				<div className="links">
					<Link to="/new_registration">New Registration</Link>
				</div>
				
				<div className="links">
					<Link to="/forgot_password">Forgot Password</Link>
				</div>
			</div>
		);
	}
}

export default Login;
