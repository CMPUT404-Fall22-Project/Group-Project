import React, { Component } from "react";
import ReactMarkdown from "react-markdown";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import axios from "axios";
import { useState } from "react";
import AuthorCardComponenet from "../author";
import { Paper, toggleButtonGroupClasses } from "@mui/material";
import { POST_TYPE_MARKDOWN, POST_TYPE_TEXT } from "../../global/postConstants";
import { MD_COMPONENETS_POST } from "../../utils/reactMarkdownComponents";
import Authentication from "../../global/authentication";
import NotificationBar from "../../global/centralNotificationBar";
import { renderPublishDate } from "../../utils/renderHelpers";

export class CommentList extends Component {
	constructor(props) {
		super(props);
		this.state = {
			isAddingComment: false,
			hasAllComments: false,
		};
	}

	supplyMoreComments() {
		// cursed
		this.props.post.requestNextComments().then(() => {
			this.setState({});
		});
	}

	moreCommentsButton() {
		if (this.props.post.getComments().length === this.props.post.getNumComments()) {
			return null;
		}
		return (
			<Button style={{ marginTop: "0.5em" }} variant="outlined" onClick={this.supplyMoreComments.bind(this)}>
				{"Load more comments..."}
			</Button>
		);
	}

	handleCommentSubmit(commentType, commentData) {
		const user = Authentication.getInstance().getUser();
		const data = {
			contentType: commentType,
			content: commentData,
			authorId: user.getId(),
		};
		axios({
			method: "post",
			url: this.props.post.getBaseData().id + "/comments/new/",
			data: data,
		})
			.then((resp) => {
				NotificationBar.getInstance().addNotification("Comment successfully posted!", NotificationBar.NT_SUCCESS);
				this.setState({ isAddingComment: false });
				window.location.reload(); // TODO: TEMP
			})
			.catch((request) => {
				NotificationBar.getInstance().addNotification("Error posting comment.", NotificationBar.NT_ERROR);
			});
	}

	handleAddComment() {
		if (!this.props.post.isLocalPost()) {
			return null;
		}
		if (!this.state.isAddingComment) {
			return (
				<Button
					variant="outlined"
					onClick={() => {
						this.setState({ isAddingComment: true });
					}}
					style={{ marginBottom: "0.5em" }}
				>
					Add a comment?
				</Button>
			);
		}
		return <CommentBox onSubmit={this.handleCommentSubmit.bind(this)}></CommentBox>;
	}

	render() {
		return (
			<div>
				{this.handleAddComment()}
				{this.props.post.getComments().map((x, idx) => (
					<div style={{ marginBottom: "0.25em" }} key={"comment" + String(idx)}>
						<CommentDisplay comment={x}></CommentDisplay>
					</div>
				))}
				{this.moreCommentsButton()}
			</div>
		);
	}
}

function renderFromChoices(contentType, content) {
	if (contentType === POST_TYPE_MARKDOWN) {
		return <ReactMarkdown escapeHtml={false} children={content} components={MD_COMPONENETS_POST}></ReactMarkdown>;
	}
	if (contentType === POST_TYPE_TEXT) {
		return <div>{content}</div>;
	}
}

const CommentDisplay = ({ comment }) => {
	return (
		<Paper variant="outlined">
			<AuthorCardComponenet data={comment.getAuthor()}></AuthorCardComponenet>
			{renderFromChoices(comment.getContentType(), comment.getContent())}
			{renderPublishDate(comment.getPublishedAt())}
		</Paper>
	);
};

// //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
// http://127.0.0.1:8000/authors/vfBSRj3SMRyZiOSiEZO67paubvcSVec7/posts/697Zu6YbI5kGnqKoB1ffM27c8qhypWqO/comments

// TODO: Make sure that comment field works
const CommentBox = (props) => {
	const [comment, commentField] = useState("");

	const handleComment = (e) => {
		props.onSubmit(POST_TYPE_TEXT, comment);
	};

	return (
		<Card variant="outlined">
			<React.Fragment>
				<CardContent>
					<TextField
						id="outlined-multiline-static"
						label="Add a comment!"
						multiline
						rows={4}
						fullWidth
						onChange={(e) => commentField(e.target.value)}
					/>
				</CardContent>
				<CardActions>
					<Button size="small" onClick={handleComment}>
						Comment
					</Button>
				</CardActions>
			</React.Fragment>
		</Card>
	);
};

export default CommentBox;
