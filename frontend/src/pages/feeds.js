import React, { Component } from "react";
import "./feeds.css";
import { Paper } from "@mui/material";
import FeedComponent, { GenericURLFeedComponenet } from "../components/genericFeed";

export default class MainFeed extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {}

	render() {
		return (
			<div className="feeds-body">
				<Paper className="feeds-background" elevation={0} variant="outlined" square>
					<div className="feeds-center" style={{ width: "30em", display: "inline-block" }}>
						<FeedComponent key={this.props.authorId} {...this.props}></FeedComponent>
					</div>
				</Paper>
			</div>
		);
	}
}

export class GenericURLFeedView extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {}

	render() {
		return (
			<div className="feeds-body">
				<Paper className="feeds-background" elevation={0} variant="outlined" square>
					<div className="feeds-center" style={{ width: "30em", display: "inline-block" }}>
						<GenericURLFeedComponenet key={this.props.url} {...this.props}></GenericURLFeedComponenet>
					</div>
				</Paper>
			</div>
		);
	}
}
