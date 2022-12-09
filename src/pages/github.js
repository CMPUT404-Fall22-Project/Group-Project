import React, { Component } from "react";
import "./feeds.css";
import { Paper, Typography } from "@mui/material";
import FeedComponent, { GenericURLFeedComponenet, GithubFeedComponent } from "../components/genericFeed";
import Authentication from "../global/authentication";
import { extractGithubName } from "../utils/githubUrl";

export default class GithubPageWrapper extends Component {
	constructor(props) {
		super(props);
		const auth = Authentication.getInstance();
		const user = auth.getUser();
		this.state = { gitUrl: extractGithubName(user) };
	}

	componentDidMount() {}

	renderInner() {
		if (!this.state.gitUrl) {
			const styles = {
				opacity: 0.5,
				padding: "1em",
			};
			return (
				<div>
					<Typography variant="h4" style={styles}>
						<i>Something went wrong...</i>
					</Typography>
					<Typography variant="h4" style={styles}>
						We couldn't parse your github URL. Make sure it is in the form: <b>https://github.com/xxxxx/</b>
					</Typography>
				</div>
			);
		}
		return (
			<GithubFeedComponent
				key={this.props.url}
				{...this.props}
				url={`https://api.github.com/users/${this.state.gitUrl}/events`}
				noLoad
			></GithubFeedComponent>
		);
	}

	render() {
		return (
			<div className="feeds-body">
				<Paper className="feeds-background" elevation={0} variant="outlined" square>
					<div className="feeds-center" style={{ width: "30em", display: "inline-block" }}>
						{this.renderInner()}
					</div>
				</Paper>
			</div>
		);
	}
}
