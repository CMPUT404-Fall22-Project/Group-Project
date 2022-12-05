import axios from "axios";
import React, { useEffect, useState } from "react";
import { Button, MenuItem } from "@mui/material";
import Box from "@mui/material/Box";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import List from "@mui/material/List";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import Grid from "@mui/material/Grid";
import Loader from "../components/loader";
import AbstractModalProvider from "./modals/modalProvider";
import ModalSystem from "../global/modalSystem";
import AccountBoxOutlinedIcon from "@mui/icons-material/AccountBoxOutlined";
import { styled } from "@mui/material/styles";

const Demo = styled("div")(({ theme }) => ({
	backgroundColor: theme.palette.background.paper,
}));

export const LikesMenuItem = ({ onClick, ...props }) => {
	return (
		<React.Fragment>
			<MenuItem
				{...props}
				onClick={() => {
					if (onClick) {
						onClick();
					}
					const provider = new LikesModal();
					provider.setProps(props.userId, props.authorId, props.postId);
					ModalSystem.getInstance().addModal("Likes-Modal", provider, {
						centered: true,
						dialog: true,
						draggable: false,
						initialHeight: "40em",
						initialWidth: "70em",
						resizable: false,
					});
				}}
			>
				Likes
			</MenuItem>
		</React.Fragment>
	);
};

class LikesModal extends AbstractModalProvider {
	constructor() {
		super();
	}

	setProps(userId, authorId, postId) {
		this.userId = userId;
		this.authorId = authorId;
		this.postId = postId;
	}

	getTitle() {
		return this.createTitleWithIcon(AccountBoxOutlinedIcon, "Likers");
	}

	getContent() {
		return <Likes userId={this.userId} authorId={this.authorId} postId={this.postId} />;
	}
}

function Likes(props) {
	const userId = props.userId;
	const authorId = props.authorId;
	const postId = props.postId;
	const [dense] = useState(false);
	const [likes, setLikes] = useState([]);
	const [isLoaded, setIsLoaded] = useState(false);

	useEffect(() => {
		handleLikes();
	}, []);

	const handleLikes = async () => {
		// Get all likes
		var response = await axios.get(`${postId}/likes/`);
		const likes = [];
		for (let like of response.data.items) {
			likes.push({ id: like.author.id, displayName: like.author.displayName, profileImage: like.author.profileImage });
		}
		setLikes(likes);
		setIsLoaded(true);
	};

	// prompt loader until likes are set
	return !isLoaded ? (
		<Loader />
	) : (
		<Box sx={{ flexGrow: 1 }}>
			<Grid container spacing={0}></Grid>
			<Grid container spacing={5}>
				<Grid item xs={12} md={0}>
					<Demo>
						<List dense={dense}>
							{likes.map((like) => (
								<ListItem>
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
	);
}
