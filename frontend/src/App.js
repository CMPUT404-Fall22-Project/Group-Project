import { Router, Route, Switch } from "react-router-dom";
import ApplicationError from "./pages/applicationError";
import HTML404 from "./components/errors/404";
import React, { Component } from "react";
import "./App.css";
import history from "./history";
import NotificationBar from "./global/centralNotificationBar";
import { AppHeader } from "./components/header/header";
import SignUpPage from "./pages/signUp";
import SignInPage from "./pages/signIn";
import Authentication from "./global/authentication";
import MainFeed, { GenericURLFeedView } from "./pages/feeds";
import EditProfile from "./components/editProfile";
import ModalSystem from "./global/modalSystem";

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
							exact
							path="/inbox/"
							render={(props) => (
								<GenericURLFeedView {...props} url={auth.getUser().getId() + "/inbox/filter/?types[]=post"} />
							)}
						/>
						<Route
							path="/posts/all/"
							render={(props) => <GenericURLFeedView {...props} url={process.env.REACT_APP_HOST + "posts/all/"} />}
						/>
						<Route
							path="/github/"
							render={(props) => <GenericURLFeedView {...props} url={process.env.REACT_APP_HOST + "github/"} />}
						/>
						<Route
							path="/authors/:id"
							render={(props) => {
								if (!props.location.state) {
									history.push("/");
									setTimeout(() => {
										NotificationBar.getInstance().addNotification(
											"Sorry, we couldn't load that data right now. Please try again later.",
											NotificationBar.NT_WARNING
										);
									}, 0);

									return <HTML404 {...props}></HTML404>;
								}
								return (
									<MainFeed {...props} author={props.location.state.author} authorId={props.location.state.author.id} />
								);
							}}
						/>
						<Route exact path="/edit-author" render={(props) => <EditProfile {...props} />} />
						<Route component={HTML404}></Route>
					</Switch>
				</Router>
			</div>
		);
	}
}

export default App;
