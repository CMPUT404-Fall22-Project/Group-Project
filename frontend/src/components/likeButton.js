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
	// var unlike = "Unlike";
	const [buttonText, setButtonText] = useState("");
	const userId = props.userId;
	const author = props.author;
	const authorId = props.author.getId();
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
			var handleLikeResponse = await axios.post(process.env.REACT_APP_HOST + "handle-like/", {
				senderAuthorURL: userId,
				receiverAuthor: { url: author.getId(), displayName: author.getUsername() },
				object: postId,
			});
			if (handleLikeResponse.status <= 201) {
				NotificationBar.getInstance().addNotification("Liked successfully!", NotificationBar.NT_SUCCESS);
				setButtonText("Liked");
			} else {
				NotificationBar.getInstance().addNotification(handleLikeResponse.err, NotificationBar.NT_ERROR);
			}
			return;
		}

		// remove userId as a liker of post
		// var response = await axios.delete(`${authorId}/inbox/`, { id: userId, type: "like" });
		// if (response.status === 200) {
		// 	setButtonText("Like");
		// } else {
		// 	NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
		// }
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
					// disabled={buttonText === "Request Sent..."}
				>
					{buttonText}
				</Button>
			</ThemeProvider>
		</div>
	);
};
