import React, { Component } from "react";
import { Button } from "@mui/material";
import { withStyles } from "@mui/styles";
import "./login.css";
import { APPLICATION_NAME } from "../constants";
import background from "../static/back.webp";
import FollowRequestSearch from "../components/followRequestSearch";

const LoginButton = withStyles((theme) => ({
	root: {
		color: "#575757",
		backgroundColor: "#ffffff",
		fontWeight: "100",
		fontSize: "0.75rem",
		width: "15em",
		height: "3em",
		"&:hover": {
			backgroundColor: "#eeeeee",
		},
	},
}))(Button);

class TestPageComponent extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {}

	login() {}

	render() {
		return (
			<div
				className="Fade-In"
				style={{
					backgroundImage: `url(${background})`,
					backgroundRepeat: "no-repeat",
					backgroundSize: "cover",
					top: "0",
					height: "100%",
					width: "100%",
					position: "absolute",
					overflow: "clip",
				}}
			>
				<div style={{ height: "100%", minHeight: "1250px", position: "relative" }}>
					<div className="outer-login-box">
						<div className="login-box">
							<div className="login-page-container">
								<div className="login-instructions">{APPLICATION_NAME}</div>

								<div style={{ padding: "1em" }}></div>
								<FollowRequestSearch variant="contained" onClick={this.login.bind(this, !this.props.check)}>
									Login
								</FollowRequestSearch>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	}
}
export default TestPageComponent;
