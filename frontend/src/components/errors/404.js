import LanguageOutlinedIcon from "@mui/icons-material/LanguageOutlined";
import HTMLError from "./errorComponent";
import React, { Component } from "react";

class HTML404 extends Component {
	render() {
		return (
			<HTMLError
				errorCode={404}
				errorDescription={"Page not found"}
				details={null}
				isFailure={false}
				icon={
					<LanguageOutlinedIcon
						className="errorIcon"
						style={{ color: "#2b7e53", fontSize: "50vh", display: "block", margin: "auto" }}
					></LanguageOutlinedIcon>
				}
			></HTMLError>
		);
	}
}

export default HTML404;
