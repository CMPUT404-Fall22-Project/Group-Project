import * as React from "react";
import { useState } from "react";
import { IconButton } from "@mui/material";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import AddCommentIcon from "@mui/icons-material/AddComment";
import axios from "axios";

const CommentDialog = (props) => {
	const { postID, authorID, baseURL } = props;

	const [open, setOpen] = React.useState(false);

	const [commentText, setComment] = useState("");

	const handleClickOpen = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};

	const addComment = () => {
		var comment = { author_id: authorID, post_id: postID, content: commentText };

		axios({
			method: "post",
			url: baseURL + "/comments",
			data: comment,
		});

		handleClose();
	};

	return (
		<span>
			<IconButton aria-label="Comment" title="Comment on above post" onClick={handleClickOpen}>
				<AddCommentIcon />
			</IconButton>
			<Dialog open={open} onClose={handleClose}>
				<DialogTitle>Add a new comment</DialogTitle>
				<DialogContent>
					<TextField
						autoFocus
						margin="dense"
						id="name"
						label="Comment"
						type="comment"
						fullWidth
						variant="standard"
						onChange={(e) => setComment(e.target.value)}
					/>
				</DialogContent>
				<DialogActions>
					<Button onClick={handleClose}>Cancel</Button>
					<Button onClick={addComment}>Comment</Button>
				</DialogActions>
			</Dialog>
		</span>
	);
};

export default CommentDialog;
