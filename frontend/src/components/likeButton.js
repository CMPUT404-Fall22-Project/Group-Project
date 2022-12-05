import { useState, useEffect } from "react";
import axios from "axios";
import cn from "classnames";
import NotificationBar from "../global/centralNotificationBar";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import Loader from "../components/loader";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Button } from "@mui/material";

const theme = createTheme({
	palette: {
		primary: {
			main: "#3366ff",
		},
	},
});

export const LikeButton = (props) => {
	var like = "Like";
	var unlike = "Unlike";
	const [buttonText, setButtonText] = useState("");
	const userId = props.userId;
	const authorId = props.authorId;
    const postId = props.postId;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// Check if author already has a pending follow request from user
		var response = await axios.get(`${authorId}/inbox/`);
		for (let item of response.data.items) {
			// Rubric states "Follow"
			if (["like"].includes(item.dataType)) {
				// if follow request sender is the user
				if (userId === item.data.id && item.data.post === postId) {
					setButtonText("Liked");
					return;
				}
			}
		}
		setButtonText("Like");
	}

	async function handleButtonClick() {
		// Handles like and unlike
		if (buttonText === "Like") {
			var response2 = await axios.post(`${authorId}/inbox/`, {id: userId, post: postId, type: "like"});
			//var response2 = await axios.post(`${authorId}/posts/${postId}/likes`, { 'id': userId, type: "like", param: "something", why: 12});
			if (response2.status === 201/* && response.status === 201*/) {
				NotificationBar.getInstance().addNotification("Liked successfully!", NotificationBar.NT_SUCCESS);
				setButtonText("Liked");
			} else {
				NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
			}
			return;
		}

		// remove userId as a liker of post
		var response = await axios.delete(`${authorId}/inbox/`, {id: userId, type: "like"});
		if (response.status === 200) {
			setButtonText("Like");
		} else {
			NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
		}
	}

	return !buttonText ? (
			<Loader />
		) : (
		<div>
			<ThemeProvider theme={theme}>
				<Button
					size="medium"
					variant="contained"
					onClick={handleButtonClick}
					disabled={buttonText === "Request Sent..."}
				>
					{buttonText}
				</Button>
			</ThemeProvider>
		</div>
	);
};
