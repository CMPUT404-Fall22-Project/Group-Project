import { useState, useEffect } from "react";
import axios from "axios";
import cn from "classnames";
import NotificationBar from "../global/centralNotificationBar";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";

export const LikeButton = (props) => {
	const [liked, setLiked] = useState(false);
	const [clicked, setClicked] = useState(false);
	const [buttonText, setButtonText] = useState("Like");
	const userId = props.userId;
	const authorId = props.authorId;
    const postId = props.postId;

	useEffect(() => {
		handleButtonText();
	}, []);

	async function handleButtonText() {
		// Check if author already has a pending follow request from user
		var response = await axios.get(`${authorId}/posts/${postId}/likes`);
		for (let item of response.data.items) {
			// Rubric states "Follow"
			if (["Like"].includes(item.type)) {
				// if follow request sender is the user
				if (userId === item.data.id) {
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
			var response = await axios.post(`${authorId}/inbox/`, { id: userId, type: "like"});
			if (response.status === 201) {
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

	return (
		<button
			onClick={() => {
				setLiked(!liked);
				setClicked(true);
				handleButtonClick()
			}}
			onAnimationEnd={() => setClicked(false)}
			className={cn("like-button-wrapper", {
				liked,
				clicked,
			})}
		>
			<div className="like-button">
				<ThumbUpIcon />
				<span>Like</span>
				<span className={cn("suffix", { liked })}>d</span>
			</div>
		</button>
	);
};
