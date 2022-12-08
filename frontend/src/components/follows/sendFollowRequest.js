import axios from "axios";
import React, { useEffect, useState } from "react";
import { Button } from "@mui/material";
import "./followRequests.css";
import Loader from "../loader";
import NotificationBar from "../../global/centralNotificationBar";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { proxiedAxios } from "../../utils/proxy";

const theme = createTheme({
	palette: {
		primary: {
			main: "#3366ff",
		},
	},
});

export const FollowRequestButton = (props) => {
	var follow = "Follow";
	var followPending = "Request Sent...";
	var following = "Following";
	const [buttonText, setButtonText] = useState("");
	const userId = props.userId;
	const author = props.author;
	const authorId = author.id;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// Check if user is already following this author
		var response = await proxiedAxios({ url: `${authorId}/followers/`, method: "get" });
		for (let author of response.data.items) {
			if (author.id === userId) {
				setButtonText(following);
				return;
			}
		}
		setButtonText(follow);
	}

	async function handleButtonClick() {
		// Sends a follow request
		if (buttonText === follow) {
			var response = await axios({
				url: process.env.REACT_APP_HOST + "handle-follow-request/",
				method: "post",
				data: {
					senderAuthorURL: userId,
					receiverAuthor: author,
				},
			});
			if (response.status <= 201) {
				NotificationBar.getInstance().addNotification("Follow request sent successfully!", NotificationBar.NT_SUCCESS);
				setButtonText(followPending);
			} else {
				NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
			}
			return;
		}
	}

	// prompt loader until buttonText is rendered
	return !buttonText ? (
		<Loader />
	) : (
		<div>
			<ThemeProvider theme={theme}>
				<Button size="medium" variant="contained" onClick={handleButtonClick} disabled={buttonText !== follow}>
					{buttonText}
				</Button>
			</ThemeProvider>
		</div>
	);
};
