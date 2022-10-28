import React, { Component } from "react";
import "./feeds.css";
import { Paper } from "@mui/material";

export default class NewPost extends Component {
	constructor(props) {
		super(props);
		this.state = {
			postType: "text/css",
		};
	}

	componentDidMount() {}
	render() {
		return (
			<div className="feeds-body">
				<Paper className="feeds-center" elevation={0} variant="outlined" />
			</div>
		);
	}
}
