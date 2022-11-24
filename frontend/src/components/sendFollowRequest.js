import axios from "axios";
import React, { useEffect, useState } from "react";
import { Button } from "@mui/material";
import "./followRequests.css";
import Loader from "../components/loader";
import NotificationBar from "../global/centralNotificationBar";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
	palette: {
		primary: {
			main: "#3366ff",
		},
	},
});

export const FollowRequestButton = (props) => {
	var follow = "Follow";
	var unfollow = "UnFollow";
	var followPending = "Request Sent...";
	const [buttonText, setButtonText] = useState("");
	const userId = props.userId;
	const authorId = props.authorId;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// Check if user is already following this author
		var response = await axios.get(`${authorId}/followers/`);
		for (let author of response.data.items) {
			if (author.id === userId) {
				setButtonText(unfollow);
				return;
			}
		}
		setButtonText(follow);
	}

	async function handleButtonClick() {
		// Handles Follow, Unfollow, and unsend
		if (buttonText === follow) {
			var response = await axios.post(`${authorId}/inbox/`, { id: userId, type: "follow" });
			if (response.status === 201) {
				NotificationBar.getInstance().addNotification("Follow request sent successfully!", NotificationBar.NT_SUCCESS);
				setButtonText(followPending);
			} else {
				NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
			}
			return;
		}
		// buttonText === "UnFollow"
		// remove userId as a follower of authorId
		var response = await axios.delete(`${authorId}/followers/${userId}`);
		if (response.status === 200) {
			setButtonText(follow);
		} else {
			NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
		}
	}

	// prompt loader until buttonText is rendered
	return !buttonText ? (
		<Loader />
	) : (
		<div>
			<ThemeProvider theme={theme}>
				<Button size="medium" variant="contained" onClick={handleButtonClick} disabled={buttonText === followPending}>
					{buttonText}
				</Button>
			</ThemeProvider>
		</div>
	);
};
