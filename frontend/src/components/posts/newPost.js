import { Button, Divider, MenuItem, Paper, Select, TextField, Typography } from "@mui/material";
import React, { Component } from "react";
import Authentication from "../../global/authentication";
import * as POST_CONSTANTS from "../../global/postConstants";
import ReactMarkdown from "react-markdown";
import DropZone from "react-dropzone";

export default class NewPost extends Component {
	constructor(props) {
		super(props);
		this.state = {
			type: POST_CONSTANTS.POST_TYPE_TEXT,
			preview: false,
			imageData: null,
			imageTypeStore: null,
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

	checkError() {}

	processFile(file) {
		const reader = new FileReader();

		if (file.type === "image/png") {
			this.setState({
				imageTypeStore: POST_CONSTANTS.POST_TYPE_PNG,
				post: { ...this.state.post, contentType: POST_CONSTANTS.POST_TYPE_PNG },
			});
		} else {
			this.setState({
				imageTypeStore: POST_CONSTANTS.POST_TYPE_JPG,
				post: { ...this.state.post, contentType: POST_CONSTANTS.POST_TYPE_JPG },
			});
		}

		reader.onload = () => {
			this.setState({ imageData: reader.result });
		};
		reader.readAsDataURL(file);
	}

	renderContent() {
		if (this.state.type === POST_CONSTANTS.POST_TYPE_PNG) {
			return (
				<div>
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
				</div>
			);
		}
		if (this.state.preview) {
			return <ReactMarkdown>{this.state.post.content || "(No content)"}</ReactMarkdown>;
		} else {
			return (
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

	handlePost() {}

	render() {
		console.log(this.state.post.contentType);
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
					}}
				>
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
							value={this.state.post.title}
							onChange={this.handleChangeGeneric.bind(this)}
						/>
						<Select
							variant="standard"
							value={this.state.type}
							onChange={(e) => this.changePostType(e.target.value)}
							style={{
								width: "20%",
								marginRight: "0.5em",
							}}
						>
							<MenuItem value={POST_CONSTANTS.POST_TYPE_TEXT}>Text</MenuItem>
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
						value={this.state.post.description}
						onChange={this.handleChangeGeneric.bind(this)}
					/>
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
