import { useState } from "react";
import cn from "classnames";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";

export const LikeButton = () => {
	const [liked, setLiked] = useState(null);
	const [clicked, setClicked] = useState(false);

export const LikeButton = (props) => {
	var like = "Like";
	var liked = "Liked";
	// var unlike = "Unlike";
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

		// UNLIKE DISABLED
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
				<Button size="medium" variant="contained" onClick={handleButtonClick} disabled={buttonText === liked}>
					{buttonText}
				</Button>
			</ThemeProvider>
		</div>
	);
};
