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
	var liked = "Liked";
	const [buttonText, setButtonText] = useState("");
	const userId = props.userId;
	const author = props.author;
	const postId = props.postId;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// get all objects (posts and comments) the user has liked
		var response = await axios.get(`${userId}` + "/liked/");
		if (response.status == 200) {
			var likedArray = response.data.items;
			// if this post is in the user's list of liked objects
			if (likedArray.find((e) => e.object === postId)) {
				setButtonText(liked);
				return;
			}
			setButtonText(like);
		}
	}

	async function handleButtonClick() {
		// Handles like and unlike
		if (buttonText === like) {
			var handleLikeResponse = await axios.post(process.env.REACT_APP_HOST + "handle-like/", {
				senderAuthorURL: userId,
				receiverAuthor: { url: author.getId(), displayName: author.getUsername() },
				object: postId,
			});
			if (handleLikeResponse.status <= 201) {
				NotificationBar.getInstance().addNotification("Liked!", NotificationBar.NT_SUCCESS);
				setButtonText(liked);
			} else {
				NotificationBar.getInstance().addNotification(handleLikeResponse.err, NotificationBar.NT_ERROR);
			}
			return;
		}
	}

	return !buttonText ? (
		<Loader />
	) : (
		<div>
			<ThemeProvider theme={theme}>
				<Button size="medium" variant="contained" onClick={handleButtonClick} disabled={buttonText === liked}>
					{buttonText}
				</Button>
			</ThemeProvider>
		</div>
	);
};
