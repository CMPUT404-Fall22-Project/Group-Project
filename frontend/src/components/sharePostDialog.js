import * as React from "react";
import { useState } from "react";
import { IconButton } from "@mui/material";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogTitle from "@mui/material/DialogTitle";
import axios from "axios";
import ShareIcon from "@mui/icons-material/Share";

const SharePostDialog = (props) => {
	const { post, author } = props;

	const [open, setOpen] = React.useState(false);

	const handleClickOpen = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};

	const sharePost = () => {
		var data = {
			id: undefined,
			title: post.title,
			description: post.description,
			content: post.content,
			contentType: post.contentType,
		};
		axios({
			method: "post",
			url: author + "/posts/",
			data: data,
		})
			.then((resp) => {
				window.location.reload();
			})
			.catch((request) => {
				console.log(request);
				window.location.reload();
			});
		handleClose();
	};

	return (
		<span>
			<IconButton aria-label="Share" title="Share above post" onClick={handleClickOpen}>
				<ShareIcon />
			</IconButton>
			<Dialog
				id="alert-dialog-title"
				aria-labelledby="alert-dialog-title"
				aria-describedby="alert-dialog-description"
				open={open}
				onClose={handleClose}
			>
				<DialogTitle id="alert-dialog-title">Share this post?</DialogTitle>
				<DialogActions>
					<Button onClick={handleClose}>Cancel</Button>
					<Button onClick={sharePost}>Share</Button>
				</DialogActions>
			</Dialog>
		</span>
	);
};

export default SharePostDialog;
