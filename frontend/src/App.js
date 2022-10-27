import { Router, Route, Switch } from "react-router-dom";
import ApplicationError from "./pages/applicationError";
import HTML404 from "./components/errors/404";
import React, { Component } from "react";
import LoginComponent from "./pages/login";
import "./App.css";
import history from "./history";
import NotificationBar from "./global/centralNotificationBar";
import { AppHeader } from "./components/header/header";
import SignUpSide from "./pages/signUp";
import SignInSide from "./pages/signIn";

class App extends Component {
	static _ERROR_DATA = [];

	constructor(props) {
		super(props);

		this.state = {};
	}

	static getDerivedStateFromError(error) {
		App._ERROR_DATA.push(error);
		return { hasError: true };
	}

	componentDidMount() {}

	render() {
		// don't touch the div it stops working if you put it in the CSS file for some reason.
		return (
			<div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
				<Router history={history}>
					<AppHeader />
					<NotificationBar />
					<Switch>
						{this.state.hasError > 0 ? (
							<Route render={(props) => <ApplicationError {...props} error={App._ERROR_DATA} />} />
						) : null}
						<Route exact path="/signup">
							<SignUpSide />
						</Route>
						<Route exact path="/signin">
							<SignInSide />
						</Route>
						<Route exact path="/" render={(props) => <LoginComponent {...props} />} />
						<Route component={HTML404}></Route>
					</Switch>
				</Router>
			</div>
		);
	}
}

export default App;
