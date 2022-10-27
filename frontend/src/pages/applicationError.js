import WarningOutlinedIcon from "@mui/icons-material/WarningOutlined";
import HTMLError from "../components/errors/errorComponent";
import React, { Component } from "react";

class ApplicationError extends Component {
	render() {
		const multiError = this.props.error.length > 1;
		const error = this.props.error[0];
		var msgExtra = "";
		if (multiError) {
			msgExtra = (
				<p>
					{String(this.props.error.length - 1)} cascaded {this.props.error.length === 2 ? "error has " : "errors have "}{" "}
					been hidden
				</p>
			);
		}
		var details = "";
		if (error.stack) {
			const t = error.stack.split("\n");
			t.splice(0, 1);
			details = (
				<h6>
					<b>--- BEGIN DEVELOPER STACK TRACE ---</b>
					{t.map((x) => {
						const msg = x;
						return <div key={msg}>{msg}</div>;
					})}
					<b>--- END DEVELOPER STACK TRACE ---</b>
				</h6>
			);
		}
		return (
			<HTMLError
				errorCode={error.name}
				errorDescription={
					<div>
						{error.message} {msgExtra}
					</div>
				}
				details={details}
				isFailure={true}
				icon={
					<WarningOutlinedIcon
						className="errorIcon"
						style={{ color: "#2b7e53", fontSize: "50vh", display: "block", margin: "auto" }}
					></WarningOutlinedIcon>
				}
			></HTMLError>
		);
	}
}

export default ApplicationError;
