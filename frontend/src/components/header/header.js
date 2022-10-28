import React, { Component } from "react";
import { Link } from "react-router-dom";

import "./header.css";

import { Avatar, MenuItem, Menu } from "@mui/material";
import { APPLICATION_NAME } from "../../constants";
import Authentication from "../../global/authentication";
import history from "../../history";
import NotificationBar from "../../global/centralNotificationBar";

const DEFAULT_HEIGHT = "56px";
export class AppHeader extends Component {
	static _instance = null;

	constructor(props) {
		super(props);

		this.state = {
			renderChild: null,
			height: DEFAULT_HEIGHT,
			userData: Authentication.getInstance().getUserSafe(),
		};
		Authentication.getInstance().addAuthChangedListener((loggedIn) => {
			this.reloadAuth();
		});
		/** @type {AppHeader} */
		AppHeader._instance = this;
	}

	reloadAuth() {
		this.setState({
			userData: Authentication.getInstance().getUserSafe(),
		});
	}

	static getInstance() {
		const inst = AppHeader._instance;
		if (!inst.state.mounted) {
			throw new Error("AppHeader not mounted");
		}
		return inst;
	}

	componentDidMount() {
		this.setState({ mounted: true });
	}

	componentWillUnmount() {
		this.setState({ mounted: false });
	}

	handleProfileClick(event) {
		this.setState({ profileMenuAnchor: event.currentTarget });
	}

	handleProfileClose() {
		this.setState({ profileMenuAnchor: null });
	}

	/**
	 * Sets a function to call on render to render extra info on the header.
	 * @param {Function} func Function which returns a react component to render
	 */
	setRenderChild(func) {
		this.setState({ renderChild: func });
	}

	removeRenderChild() {
		this.setState({ renderChild: null });
	}

	setHeaderHeight(height = null) {
		if (height === null) {
			height = DEFAULT_HEIGHT;
		}
		this.setState({ maxHeight: height });
	}

	logout() {
		Authentication.getInstance()
			.logout()
			.then(() => {
				history.push("/");
				NotificationBar.getInstance().addNotification("Successfully logged out", NotificationBar.NT_SUCCESS);
				this.handleProfileClose();
			});
	}

	render() {
		const auth = Authentication.getInstance();
		return (
			<div
				className="topnav"
				style={{
					transition: "height 0.5s ease-in-out",
					height: this.state.height,
					minHeight: this.state.height,
				}}
			>
				<div>
					{/* Return users back to home page on logo click*/}

					<div className="title-container">
						<Link to="/" style={{ textDecoration: "none" }}>
							<span style={{ whiteSpace: "nowrap" }} className="title">
								{APPLICATION_NAME}
							</span>
						</Link>
					</div>
				</div>
				{this.state.renderChild ? this.state.renderChild() : null}
				<div className="topnav-toolbar-container">
					<span style={{ whiteSpace: "nowrap", fontWeight: "600", color: "#ffffff" }}>
						{this.state.userData.getUsername()}
					</span>
					<Avatar
						onClick={this.handleProfileClick.bind(this)}
						style={{ marginLeft: "0.5em", cursor: "pointer" }}
						src={this.state.userData.getProfileImageUrl()}
						alt={this.state.userData.getUsername()}
					></Avatar>
					<Menu
						anchorOrigin={{
							vertical: "bottom",
							horizontal: "right",
						}}
						transformOrigin={{
							vertical: "top",
							horizontal: "right",
						}}
						anchorEl={this.state.profileMenuAnchor}
						keepMounted
						open={Boolean(this.state.profileMenuAnchor)}
						onClose={this.handleProfileClose.bind(this)}
					>
						<MenuItem disabled={!auth.isLoggedIn()} variant="outlined" onClick={this.logout.bind(this)}>
							Logout
						</MenuItem>
					</Menu>
				</div>
			</div>
		);
	}
}
export default AppHeader;