import React, { Component } from "react";
import "./feeds.css";
import { Paper } from "@mui/material";
import MyFeed from "../components/myFeed";

export default class MainFeed extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {}

	render() {
		return (
			<div className="feeds-body">
				<Paper className="feeds-center" elevation={0} variant="outlined" square>
					<MyFeed></MyFeed>
				</Paper>
			</div>
		);
	}
}
