import { Divider, IconButton, Paper, Typography } from "@mui/material";
import React, { Component } from "react";
import { POST_TYPE_JPG, POST_TYPE_MARKDOWN, POST_TYPE_PNG, POST_TYPE_TEXT } from "../../global/postConstants";
import AuthorCardComponenet from "../author";
import ReactMarkdown from "react-markdown";
import { MD_COMPONENETS_POST } from "../../utils/reactMarkdownComponents";
import PostEditor from "./newPost";
import ModeEditOutlineOutlinedIcon from "@mui/icons-material/ModeEditOutlineOutlined";
import DeleteOutlineOutlinedIcon from "@mui/icons-material/DeleteOutlineOutlined";
import Authentication from "../../global/authentication";
import ModalTemplates from "../modals/genericModalTemplates";
import axios from "axios";
import CommentDialog from "./../commentDialog";
import ScrollDialog from "../commentViewDialog";
import { CommentList } from "../comments/comment";
import { renderPublishDate } from "../../utils/renderHelpers";
import LinkOutlinedIcon from "@mui/icons-material/LinkOutlined";
import NotificationBar from "../../global/centralNotificationBar";
import { tryStringifyObject } from "../../utils/stringify";
import ShareIcon from "@mui/icons-material/Share";
import SharePostDialog from "../sharePostDialog";

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

	handleCopyLink() {
		const data = this.props.data.getBaseData();
		var url = "";
		if (data.contentType.startsWith("image")) {
			url = data.id + "/image";
		} else {
			var u = new URL(data.id);
			url = window.location.host + u.pathname;
		}
		navigator.clipboard
			.writeText(url)
			.then(() => {
				NotificationBar.getInstance().addNotification("Link copied to clipboard", NotificationBar.NT_SUCCESS);
			})
			.catch((err) => {
				NotificationBar.getInstance().addNotification(
					"Failed to copy link: " + tryStringifyObject(err),
					NotificationBar.NT_ERROR
				);
			});
	}

	render() {
		return (
			<div
				style={{
					marginTop: "1em",
					opacity: this.props.data.getBaseData().unlisted ? 0.5 : 1,
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
						{this.props.data.isLocalPost() && this.props.data.getBaseData().contentType.startsWith("image") ? (
							<IconButton aria-label="Options" title="Copy URL..." onClick={this.handleCopyLink.bind(this)}>
								<LinkOutlinedIcon />
							</IconButton>
						) : null}
					</Typography>
					<Typography variant="caption">
						<i>{this.props.data.getBaseData().description}</i>
					</Typography>
					<Divider></Divider>
					{this.renderFromChoices()}
					<Divider></Divider>
					{renderPublishDate(this.props.data.getBaseData().published)}
					{this.props.children}
				</Paper>
			</div>
		);
	}
}

export class EditablePostContainer extends Component {
	constructor(props) {
		super(props);
		this.state = { editMode: false };
	}

	isEditable() {
		if (this.props.isEditableFunc) {
			return this.props.isEditableFunc(this.props.data);
		}
		const id = Authentication.getInstance().getUser().getId();
		const data = this.props.data.getBaseData();
		return data.author.getId() === id;
	}

	tryDeletePost() {
		ModalTemplates.confirm("Delete Post?", "Are you sure you want to delete this post?").then((result) => {
			if (result === ModalTemplates.RESULT_SUCCESS) {
				axios({
					method: "delete",
					url: this.props.data.getBaseData().origin,
				}).then(() => window.location.reload());
			}
		});
	}

	render() {
		var comp = null;
		if (this.state.editMode) {
			comp = (
				<PostEditor
					prefillData={this.props.data.getBaseData()}
					overrideName="Edit Post..."
					onClose={() => {
						window.location.reload(); // TEMP. VERY BAD!!!
					}}
				></PostEditor>
			);
		} else {
			comp = <PostViewComponent data={this.props.data}></PostViewComponent>;
		}

		if (!this.isEditable()) {
			return (
				<div>
					{comp}
					<CommentDialog
						postID={this.props.data.getBaseData().id}
						authorID={Authentication.getInstance().getUser().getId()}
						baseURL={this.props.data.getBaseData().origin}
					/>
					<ScrollDialog baseURL={this.props.data.getBaseData().origin} comments={this.props.data.getComments()} />
					<SharePostDialog
						post={this.props.data.getBaseData()}
						author={Authentication.getInstance().getUser().getId()}
					/>
				</div>
			);
		}

		return (
			<React.Fragment>
				{comp}
				<IconButton
					aria-label="Follow"
					title="Edit above post"
					onClick={() => this.setState({ editMode: !this.state.editMode })}
				>
					<ModeEditOutlineOutlinedIcon />
				</IconButton>
				<IconButton aria-label="Delete" title="Delete above post" onClick={this.tryDeletePost.bind(this)}>
					<DeleteOutlineOutlinedIcon />
				</IconButton>
				<CommentDialog
					postID={this.props.data.getBaseData().id}
					authorID={Authentication.getInstance().getUser().getId()}
					baseURL={this.props.data.getBaseData().origin}
				/>
				<ScrollDialog baseURL={this.props.data.getBaseData().origin} comments={this.props.data.getComments()} />
				<SharePostDialog post={this.props.data.getBaseData()} author={Authentication.getInstance().getUser().getId()} />
			</React.Fragment>
		);
	}
}
