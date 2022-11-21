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
	const [buttonText, setButtonText] = useState("");
	const userId = props.userId;
	const authorId = props.authorId;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// Check if author already has a pending follow request from user
		var response = await axios.get(`${authorId}/inbox/`);
		for (let item of response.data.items) {
			// Rubric states "Follow"
			if (["Follow", "follow"].includes(item.dataType)) {
				// if follow request sender is the user
				console.log("actor.id: ", item.data.actor.id);
				console.log("userId: ", userId);
				if (userId === item.data.actor.id) {
					setButtonText("Request Sent...");
					return;
				}
			}
		}
		// Check if user is already following this author
		var response = await axios.get(`${userId}/following/`);
		console.log(response);
		for (let author of response.data.items) {
			if (author.id === authorId) {
				setButtonText("UnFollow");
				return;
			}
		}
		setButtonText("Follow");
	}

	async function handleButtonClick() {
		// Handles Follow, Unfollow, and unsend
		if (buttonText === "Follow") {
			var response = await axios.post(`${authorId}/inbox/`, { id: userId, type: "follow" });
			if (response.status === 201) {
				NotificationBar.getInstance().addNotification("Follow request sent successfully!", NotificationBar.NT_SUCCESS);
				setButtonText("Request Sent...");
			} else {
				NotificationBar.getInstance().addNotification(response.err, NotificationBar.NT_ERROR);
			}
			return;
		}
		// buttonText === "UnFollow"
		// remove userId as a follower of authorId
		var response = await axios.put(`${authorId}/followers/${userId}`);
		if (response.status === 200) {
			NotificationBar.getInstance().addNotification(
				`You are no longer following ${authorId}`,
				NotificationBar.NT_SUCCESS
			);
			setButtonText("Follow");
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
