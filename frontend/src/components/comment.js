import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import axios from "axios";
import { useState } from "react";

// //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
// http://127.0.0.1:8000/authors/vfBSRj3SMRyZiOSiEZO67paubvcSVec7/posts/697Zu6YbI5kGnqKoB1ffM27c8qhypWqO/comments

// TODO: Make sure that comment field works
const CommentBox = (props) => {
	const { postID, displayName } = props;

	const [comment, commentField] = useState("");

	const commentJSON = { comment };

	const handleComment = (e) => {
		axios({
			method: "post",
			url: "service/authors/" + displayName + "/posts/" + postID + "/comments",
			data: commentJSON, // not sure if more data is needed?
		})
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
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
