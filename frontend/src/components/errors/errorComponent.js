import React, { Component } from "react";
import history from "../../history";
import { Divider } from "@mui/material";

class HTMLError extends Component {
	constructor(props) {
		super(props);
		this.state = {
			...props,
		};
	}

	returnToHome() {
		if (this.state.isFailure) {
			window.location.reload();
			return;
		}
		history.push({
			pathname: "/",
		});
	}

	render() {
		return (
			<div style={{ backgroundColor: "#fafafa", height: "100%" }}>
				<div
					style={{
						textAlign: "center",
						fontSize: "1.25em",
						width: "100%",
						color: "#5e5e5e",
						marginLeft: "auto",
						marginRight: "auto",
						marginTop: "5vh",
					}}
				>
					<strong
						style={{
							color: "#2e2e2e",
							fontSize: "5em",
						}}
					>
						{this.state.errorCode}
					</strong>
					<br></br>
					<i
						style={{
							fontSize: "1.2em",
						}}
					>
						{this.state.errorDescription}
					</i>
					{this.state.details !== undefined ? (
						<div style={{ marginTop: "1em", marginBottom: "1em" }}>{this.state.details}</div>
					) : (
						<div style={{ marginTop: "1em", marginBottom: "1em" }}>No additional details are known</div>
					)}
					{this.state.isFailure ? (
						<div style={{ marginTop: "1em", marginBottom: "1em" }}>
							<strong>Fix your code!!! (see console for more line numbers)</strong>
						</div>
					) : null}
					<button
						onClick={this.returnToHome.bind(this)}
						style={{
							fontSize: "0.8em",
						}}
					>
						{this.state.isFailure ? "Reload application" : "Return to homepage"}
					</button>
				</div>
				<Divider style={{ width: "50%", marginTop: "1em", marginLeft: "auto", marginRight: "auto" }}></Divider>
				{this.state.icon}
			</div>
		);
	}
}

export default HTMLError;
