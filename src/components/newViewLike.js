import axios from "axios";
import React, { useEffect, useState } from "react";
import EmojiEmotionsIcon from "@mui/icons-material/EmojiEmotions";
import { IconButton } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import Grid from "@mui/material/Grid";
import { styled } from "@mui/material/styles";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";

const Demo = styled("div")(({ theme }) => ({
	backgroundColor: theme.palette.background.paper,
}));

export default function NewViewLike(props) {
	const { postId } = props;
	const [open, setOpen] = React.useState(false);
	const [dense] = useState(false);
	const [likes, setLikes] = useState([]);
	const [scroll, setScroll] = React.useState("paper");

	const handleClickOpen = () => {
		handleLikes();
		setOpen(true);
		setScroll("body");
	};

	const handleClose = () => {
		setOpen(false);
	};

	const handleLikes = async () => {
		// Get all likes
		var response = await axios.get(`${postId}/likes/`);
		console.log(postId);
		const authors = [];
		for (let like of response.data.items) {
			authors.push(like.author);
		}
		var likes = [];
		for (let author of authors) {
			var response = await axios.get(`${author}`);
			likes.push({
				id: response.data.id,
				displayName: response.data.displayName,
				profileImage: response.data.profileImage,
			});
		}
		setLikes(likes);
	};
	return (
		<React.Fragment>
			<IconButton aria-label="Like" title="Like above post" type="button" onClick={handleClickOpen}>
				<EmojiEmotionsIcon />
			</IconButton>
			<Dialog
				open={open}
				onClose={handleClose}
				scroll={scroll}
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
			>
				<DialogTitle id="scroll-dialog-title">Likes</DialogTitle>
				<DialogContent dividers={scroll === "body"} id="commentList">
					<Box sx={{ flexGrow: 1 }}>
						<Grid container spacing={5}>
							<Grid item xs={12} md={0}>
								<Demo>
									<List dense={dense}>
										{likes.map((like) => (
											<ListItem key={like.id}>
												<ListItemAvatar>
													<Avatar alt="actor" src={like.profileImage}></Avatar>
												</ListItemAvatar>
												<ListItemText primary={like.displayName} key={like.id} />
											</ListItem>
										))}
									</List>
								</Demo>
							</Grid>
						</Grid>
					</Box>
				</DialogContent>
			</Dialog>
		</React.Fragment>
	);
}
