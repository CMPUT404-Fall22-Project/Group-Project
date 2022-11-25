import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import ListItem from "@mui/material/ListItem";

// https://levelup.gitconnected.com/fetch-api-data-with-axios-and-display-it-in-a-react-app-with-hooks-3f9c8fa89e7b

export default function CommentListItem(props) {
	const displayComments = (props) => {
		const { comments, author } = props;
		if (comments.length > 0) {
			return comments.map((comment) => {
				const date = new Date(comment.published);
				return (
					<ListItem alignItems="flex-start" key={comment.id}>
						<ListItemAvatar>
							<Avatar alt="Remy Sharp" src={author.profileImage} />
						</ListItemAvatar>
						<ListItemText
							primary={author.displayName}
							secondary={
								<React.Fragment>
									<Typography sx={{ display: "inline" }} component="span" variant="body2" color="text.primary">
										{date.toLocaleDateString() + " - " + date.toLocaleTimeString()}
									</Typography>
									{" — " + comment.content}
								</React.Fragment>
							}
						/>
					</ListItem>
				);
			});
		} else {
			return <p>There are no comments for this post. </p>;
		}
	};

	return <>{displayComments(props)}</>;
}
