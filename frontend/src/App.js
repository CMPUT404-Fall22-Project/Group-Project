import { Router, Route, Switch } from "react-router-dom";
import ApplicationError from "./pages/applicationError";
import HTML404 from "./components/errors/404";
import React, { Component } from "react";
import Test from "./pages/test";
import LoginComponent from "./pages/login";
import TestPageComponent from "./pages/testPage";
import "./App.css";
import history from "./history";
import FollowRequestSearch from "./components/followRequestSearch";
import NotificationBar from "./global/centralNotificationBar";
import { AppHeader } from "./components/header/header";
import SignUpPage from "./pages/signUp";
import SignInPage from "./pages/signIn";
import Authentication from "./global/authentication";
import MainFeed from "./pages/feeds";
import EditProfile from "./components/editProfile";
import ModalSystem from "./global/modalSystem";
import { FollowRequestsButton } from "./components/followRequests";

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
					<ModalSystem></ModalSystem>
					<AppHeader />
					<NotificationBar />
					<Switch>
						{this.state.hasError > 0 ? (
							<Route render={(props) => <ApplicationError {...props} error={App._ERROR_DATA} />} />
						) : null}
						<Route exact path="/signup" render={(props) => <SignUpPage {...props} />} />
						{!auth.isLoggedIn() ? <Route render={(props) => <SignInPage {...props} />} /> : null}
						<Route exact path="/" render={(props) => <MainFeed {...props} authorId={auth.getUser().getId()} />} />
						<Route
							path="/authors/:id"
							render={({ match, ...props }) => <MainFeed {...props} authorId={match.params.id} />}
						/>
						{/* <Route exact path="/amrit" render={(props) => <FollowRequestsButton {...props} />} /> */}
						<Route exact path="/temp-follow-request" render={(props) => <FollowRequestSearch {...props} />} />

						<Route exact path="/zaza" render={(props) => <EditProfile {...props} />} />
						<Route component={HTML404}></Route>
					</Switch>
				</Router>
			</div>
		);
	}
}

export default App;
