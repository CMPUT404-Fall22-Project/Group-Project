import { useState, useEffect } from "react";
import axios from "axios";
import NotificationBar from "../global/centralNotificationBar";
import Loader from "../components/loader";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Button } from "@mui/material";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import { IconButton } from "@mui/material";

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
	const sourceId = props.sourceId;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// get all objects (posts and comments) the user has liked
		var response = await axios.get(`${userId}` + "/liked/");
		if (response.status == 200) {
			var likedArray = response.data.items;
			// if this post is in the user's list of liked objects
			if (likedArray.find((e) => e.object === sourceId)) {
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
				receiverAuthor: { url: getAuthorId(), displayName: getAuthorDisplayName() },
				object: sourceId,
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

	function getAuthorId() {
		try {
			return author.getId();
		} catch (err) {
			return author.id;
		}
	}
	function getAuthorDisplayName() {
		try {
			author.getUsername();
		} catch (err) {
			return author.displayName;
		}
	}

	return !buttonText ? (
		<Loader />
	) : (
		<span>
			<ThemeProvider theme={theme}>
				<IconButton
					aria-label="Like"
					title="Like above post"
					type="button"
					onClick={handleButtonClick}
					disabled={buttonText === liked}
				>
					<ThumbUpIcon />
				</IconButton>
			</ThemeProvider>
		</span>
	);
};
