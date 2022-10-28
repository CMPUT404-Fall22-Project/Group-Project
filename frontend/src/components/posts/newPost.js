import {
	Backdrop,
	Button,
	Checkbox,
	Divider,
	FormControlLabel,
	MenuItem,
	Paper,
	Select,
	TextField,
	Typography,
} from "@mui/material";
import React, { Component } from "react";
import Authentication from "../../global/authentication";
import * as POST_CONSTANTS from "../../global/postConstants";
import ReactMarkdown from "react-markdown";
import DropZone from "react-dropzone";
import NotificationBar from "../../global/centralNotificationBar";
import TagInput from "../tagInput";
import axios from "axios";
import Loader from "../loader";
import ContainedBackdrop from "../../utils/containedBackdrop";
import { MD_COMPONENETS_POST } from "../../utils/reactMarkdownComponents";

export default class NewPost extends Component {
	constructor(props) {
		super(props);
		this.state = {
			type: POST_CONSTANTS.POST_TYPE_TEXT,
			preview: false,
			imageData: null,
			imageTypeStore: null,
			isPosting: false,
			post: {
				title: "New Post",
				description: "",
				content: "",
				contentType: POST_CONSTANTS.POST_TYPE_TEXT,
				author: Authentication.getInstance().getUser().copy(),
				categories: [],
				visibility: POST_CONSTANTS.POST_VISIBILITY_PUBLIC,
				unlisted: false,
			},
		};
	}

	componentDidMount() {}

	handleChangeGeneric(event) {
		this.setState((prevState) => {
			return {
				post: {
					...prevState.post,
					[event.target.name]: event.target.value,
				},
			};
		});
	}

	processFile(file) {
		const reader = new FileReader();

		const type = file.type === "image/png" ? POST_CONSTANTS.POST_TYPE_PNG : POST_CONSTANTS.POST_TYPE_JPG;

		const newState = {
			imageTypeStore: type,
			post: {
				...this.state.post,
				contentType: this.state.type === POST_CONSTANTS.POST_TYPE_PNG ? type : this.state.post.contentType,
			},
		};

		if (this.state.post.contentType === POST_CONSTANTS.POST_TYPE_TEXT) {
			newState.post.contentType = POST_CONSTANTS.POST_TYPE_MARKDOWN;
			newState.type = POST_CONSTANTS.POST_TYPE_MARKDOWN;
		}

		this.setState(newState);

		reader.onload = () => {
			this.setState({ imageData: reader.result });
		};
		reader.readAsDataURL(file);
	}

	handleComplete() {
		if (this.props.onClose) {
			this.props.onClose();
		}
	}

	renderContent() {
		const imgComponent = (
			<DropZone
				accept={{ "image/png": [], "image/jpeg": [] }}
				maxFiles={1}
				onDropAccepted={(file) => this.processFile(file[0])}
			>
				{({ getRootProps, getInputProps }) => (
					<section>
						<div {...getRootProps()} style={{ border: "solid black 1px", margin: "0.5em" }}>
							<input {...getInputProps()} />
							<p>Drag and drop or click to upload images.</p>
							{this.state.imageData ? <img src={this.state.imageData} width="80%"></img> : null}
						</div>
					</section>
				)}
			</DropZone>
		);
		if (this.state.preview) {
			return (
				<React.Fragment>
					<ReactMarkdown components={MD_COMPONENETS_POST}>{this.state.post.content || "(No content)"}</ReactMarkdown>
					{imgComponent}
				</React.Fragment>
			);
		} else {
			if (this.state.type === POST_CONSTANTS.POST_TYPE_PNG) {
				return imgComponent;
			}
			return (
				<React.Fragment>
					<TextField
						style={{
							margin: "0.5em",
						}}
						name="content"
						multiline
						id="content"
						label=""
						value={this.state.post.content}
						onChange={this.handleChangeGeneric.bind(this)}
					/>
					{imgComponent}
				</React.Fragment>
			);
		}
	}

	changePostType(newType) {
		if (newType === POST_CONSTANTS.POST_TYPE_PNG) {
			this.setState({
				type: newType,
				post: { ...this.state.post, contentType: this.state.imageTypeStore },
			});
		} else {
			this.setState({
				type: newType,
				post: { ...this.state.post, contentType: newType },
			});
		}
	}

	sendPostRequest(data, postURL) {
		return new Promise((resolve, reject) => {
			axios({
				method: "post",
				url: postURL,
				withCredentials: true,
				data: data,
			})
				.then((resp) => {
					resolve(resp.data.id);
				})
				.catch((request) => {
					reject(request);
				});
		});
	}

	handleImagePost(data) {
		this.setState({ isPosting: true });
		const url = Authentication.getInstance().getUser().getUrl() + "/posts/";
		data.content = data.content.split(",")[1];
		this.sendPostRequest(data, url).then(this.handleComplete.bind(this));
	}

	handleTextPost(data) {
		this.setState({ isPosting: true });
		const url = Authentication.getInstance().getUser().getUrl() + "/posts/";
		if (this.state.imageData) {
			const data2 = {
				content: this.state.imageData.split(",")[1],
				contentType: this.state.imageTypeStore,
				description: "",
				title: "ImageUpload" + Math.floor(Math.random() * (1 << 24)),
				visibility: this.state.post.visibility,
				unlisted: true,
				description: "Image upload",
				author: Authentication.getInstance().getUser().copy(),
				categories: [],
			};
			this.sendPostRequest(data2, url).then((id) => {
				data.content += `\n![](${url}${id}/image)`;
				this.sendPostRequest(data, url).then(this.handleComplete.bind(this));
			});
		} else {
			this.sendPostRequest(data, url).then(this.handleComplete.bind(this));
		}
	}

	handlePost() {
		if (!this.state.post.title) {
			return;
		}
		const data = {
			...this.state.post,
		};
		if (this.state.type === POST_CONSTANTS.POST_TYPE_PNG) {
			if (this.state.imageData === null) {
				NotificationBar.getInstance().addNotification("You must supply an image!", NotificationBar.NT_ERROR);
				return;
			}
			data.content = this.state.imageData;
			this.handleImagePost(data);
		} else {
			this.handleTextPost(data);
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
						position: "relative",
					}}
				>
					<ContainedBackdrop open={this.state.isPosting}>
						<Loader></Loader>
					</ContainedBackdrop>

					<Typography variant="h5">
						<i>Create a new post...</i>
					</Typography>
					<Divider></Divider>
					<div
						style={{
							display: "flex",
							alignItems: "baseline",
						}}
					>
						<TextField
							style={{
								width: "80%",
								margin: "0.5em",
							}}
							name="title"
							margin="dense"
							variant="standard"
							required
							id="title"
							label="Title"
							size="small"
							value={this.state.post.title}
							onChange={this.handleChangeGeneric.bind(this)}
							error={!this.state.post.title}
						/>
						<Select
							variant="standard"
							value={this.state.type}
							onChange={(e) => this.changePostType(e.target.value)}
							size="small"
							style={{
								width: "20%",
								marginRight: "0.5em",
							}}
						>
							{this.state.imageData ? null : <MenuItem value={POST_CONSTANTS.POST_TYPE_TEXT}>Text</MenuItem>}
							<MenuItem value={POST_CONSTANTS.POST_TYPE_MARKDOWN}>Markdown</MenuItem>
							<MenuItem value={POST_CONSTANTS.POST_TYPE_PNG}>Image</MenuItem>
						</Select>
					</div>
					<TextField
						style={{
							marginLeft: "0.5em",
							marginRight: "0.5em",
						}}
						name="description"
						margin="dense"
						variant="standard"
						id="description"
						label="Description"
						size="small"
						value={this.state.post.description}
						onChange={this.handleChangeGeneric.bind(this)}
						error={!this.state.post.description}
					/>
					<div
						style={{
							display: "flex",
							alignItems: "center",
						}}
					>
						<TagInput
							style={{
								width: "95%",
								margin: "0.5em",
							}}
							value={this.state.post.categories}
							onChange={(newValue) => {
								this.setState({ post: { ...this.state.post, categories: newValue } });
							}}
							placeholder="Categories"
						></TagInput>
						<Select
							variant="standard"
							name="visibility"
							value={this.state.post.visibility}
							onChange={this.handleChangeGeneric.bind(this)}
							size="small"
							style={{
								width: "20%",
								marginRight: "0.5em",
							}}
						>
							<MenuItem value={POST_CONSTANTS.POST_VISIBILITY_PUBLIC}>Public</MenuItem>
							<MenuItem value={POST_CONSTANTS.POST_VISIBILITY_FRIENDS}>Friends</MenuItem>
						</Select>
						<FormControlLabel
							style={{
								width: "15%",
							}}
							control={<Checkbox value={this.state.post.unlisted} onChange={this.handleChangeGeneric.bind(this)} />}
							label="Unlisted"
						/>
					</div>

					{this.renderContent()}
					<div
						style={{
							display: "flex",
							justifyContent: "space-around",
							marginBottom: "1.5em",
						}}
					>
						{this.state.type === POST_CONSTANTS.POST_TYPE_MARKDOWN ? (
							<Button
								variant="contained"
								color="primary"
								onClick={() => this.setState({ preview: !this.state.preview })}
							>
								Toggle Preview
							</Button>
						) : null}

						<Button variant="contained" color="primary" onClick={() => this.handlePost()}>
							Post!
						</Button>
					</div>
				</Paper>
			</div>
		);
	}
}

export class NewPostButton extends Component {
	constructor(props) {
		super(props);
		this.state = {
			isOpen: false,
		};
	}

	render() {
		if (this.state.isOpen) {
			return (
				<NewPost
					onClose={() => {
						this.setState({ isOpen: false });
					}}
				></NewPost>
			);
		} else {
			return <Button onClick={() => this.setState({ isOpen: true })}>Create new post</Button>;
		}
	}
}
