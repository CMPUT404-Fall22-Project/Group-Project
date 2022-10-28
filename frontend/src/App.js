import { Router, Route, Switch } from "react-router-dom";
import ApplicationError from "./pages/applicationError";
import HTML404 from "./components/errors/404";
import React, { Component } from "react";
import Test from "./pages/test";
import LoginComponent from "./pages/login";
import TestPageComponent from "./pages/testPage";
import "./App.css";
import history from "./history";
import FollowRequest from "./components/followRequest";
import NotificationBar from "./global/centralNotificationBar";
import { AppHeader } from "./components/header/header";
import SignUpPage from "./pages/signUp";
import SignInPage from "./pages/signIn";
import Authentication from "./global/authentication";
import MainFeed from "./pages/feeds";

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

	componentDidMount() {
		Authentication.getInstance().addAuthChangedListener(() => {
			this.setState({});
		});
	}

	render() {
		// don't touch the div it stops working if you put it in the CSS file for some reason.
		const auth = Authentication.getInstance();
		return (
			<div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
				<Router history={history}>
					<AppHeader />
					<NotificationBar />
					<Switch>
						{this.state.hasError > 0 ? (
							<Route render={(props) => <ApplicationError {...props} error={App._ERROR_DATA} />} />
						) : null}
						<Route exact path="/signup" render={(props) => <SignUpPage {...props} />} />
						{!auth.isLoggedIn() ? <Route render={(props) => <SignInPage {...props} />} /> : null}
						<Route exact path="/" render={(props) => <MainFeed {...props} />} />
						<Route exact path="/amrit" render={(props) => <Test {...props} />} />
						<Route exact path="/temp-follow-request" render={(props) => <FollowRequest {...props} />} />

						<Route component={HTML404}></Route>
					</Switch>
				</Router>
			</div>
		);
	}
}

export default App;
