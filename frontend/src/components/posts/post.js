import { Divider, Paper, Typography } from "@mui/material";
import React, { Component } from "react";
import { POST_TYPE_JPG, POST_TYPE_MARKDOWN, POST_TYPE_PNG, POST_TYPE_TEXT } from "../../global/postConstants";
import AuthorCardComponenet from "../author";
import ReactMarkdown from "react-markdown";
import { MD_COMPONENETS_POST } from "../../utils/reactMarkdownComponents";

export default class PostViewComponent extends Component {
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
			return <ReactMarkdown escapeHtml={false} children={d.content} components={MD_COMPONENETS_POST}></ReactMarkdown>;
		}
		if (d.contentType === POST_TYPE_TEXT) {
			return <p>{d.content}</p>;
		}
	}

	renderDate(date) {
		const d = new Date(date);
		return (
			<Typography variant="caption">
				<i>Published at {d.toLocaleDateString() + " - " + d.toLocaleTimeString()}</i>
			</Typography>
		);
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
					<AuthorCardComponenet data={this.props.data.getAuthor()}></AuthorCardComponenet>
					<Typography variant="h5">
						<i>{this.props.data.getBaseData().title}</i>
					</Typography>
					<Typography variant="caption">
						<i>{this.props.data.getBaseData().description}</i>
					</Typography>
					<Divider></Divider>
					{this.renderFromChoices()}
					<Divider></Divider>
					{this.renderDate(this.props.data.getBaseData().published)}
				</Paper>
			</div>
		);
	}
}
