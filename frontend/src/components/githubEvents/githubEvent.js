import { Divider, Paper, Typography } from "@mui/material";
import React, { Component } from "react";
import { POST_TYPE_JPG, POST_TYPE_MARKDOWN, POST_TYPE_PNG, POST_TYPE_TEXT } from "../../global/postConstants";
import ReactMarkdown from "react-markdown";
import { MD_COMPONENETS_POST } from "../../utils/reactMarkdownComponents";
import { renderPublishDate } from "../../utils/renderHelpers";

export default class GithubEventComponent extends Component {
	constructor(props) {
		super(props);
		if (!props.data) {
			throw new Error("Missing required prop 'data'");
		}
	}

	renderFromChoices() {
		const d = this.props.data.getBaseData();
		if (d.contentType === POST_TYPE_JPG || d.contentType === POST_TYPE_PNG) {
			return <img src={"data:" + d.contentType + "," + d.content} width="80%" style={{ margin: "auto" }}></img>;
		}
		if (d.contentType === POST_TYPE_MARKDOWN) {
			return;
		}
		if (d.contentType === POST_TYPE_TEXT) {
			return <p>{d.content}</p>;
		}
	}
	render() {
		return (
			<div
				style={{
					marginTop: "1em",
				}}
			>
				<Paper
					variant="outlined"
					style={{
						width: "90%",
						margin: "auto",
						display: "flex",
						flexDirection: "column",
						padding: "0.5em",
					}}
				>
					<Typography variant="h5">
						<i>{this.props.data.getTitle()}</i>
					</Typography>
					<Typography variant="caption">
						<i>{"Github event."}</i>
					</Typography>
					<Divider></Divider>
					<ReactMarkdown
						escapeHtml={false}
						children={this.props.data.getMessage()}
						components={MD_COMPONENETS_POST}
					></ReactMarkdown>
					<Divider></Divider>
					{renderPublishDate(this.props.data.getPublished())}
					{this.props.children}
				</Paper>
			</div>
		);
	}
}
