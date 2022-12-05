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
import Stack from "@mui/material/Stack";
import Authentication from "../global/authentication";
import Loader from "./loader";
import AbstractModalProvider from "./modals/modalProvider";
import ModalSystem from "../global/modalSystem";
import AccountBoxOutlinedIcon from "@mui/icons-material/AccountBoxOutlined";
import NotificationBar from "../global/centralNotificationBar";
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
					const provider = new FollowRequestsModal();
					ModalSystem.getInstance().addModal("Follow-Requests-Modal", provider, {
						centered: true,
						dialog: true,
						draggable: false,
						initialHeight: "40em",
						initialWidth: "70em",
						resizable: false,
					});
				}}
			>
				Follow Requests
			</MenuItem>
		</React.Fragment>
	);
};

class FollowRequestsModal extends AbstractModalProvider {
	constructor() {
		super();
	}

	getTitle() {
		return this.createTitleWithIcon(AccountBoxOutlinedIcon, "Follow Requests");
	}

	getContent() {
		return <FollowRequests></FollowRequests>;
	}
}

export function FollowRequests() {
	const userId = Authentication.getInstance().getUser().getId();
	const [dense] = useState(false);
	const [followRequests, setFollowRequests] = useState([]);
	const [followerIds, setFollowerIds] = useState([]);
	const [isLoaded, setIsLoaded] = useState(false);

	useEffect(() => {
		handleFollowRequests();
	}, []);

	const handleFollowRequests = async () => {
		// Get all followers
		response = await axios.get(`${userId}/followers/`);
		console.log(response);
		const followerIds = [];
		for (let follower of response.data.items) {
			followerIds.push(follower.id);
		}
		setFollowerIds(followerIds);

		// Get all follow requests
		var response = await axios.get(`${userId}/inbox/`);
		console.log(response);
		const followRequests = [];
		for (let item of response.data.items) {
			// Rubric states "Follow"
			if (["Follow", "follow"].includes(item.dataType)) {
				followRequests.push(item);
			}
		}
		setFollowRequests(followRequests);
		setIsLoaded(true);
	};

	async function handleAcceptButton(followRequest) {
		// PUT the Author with id === followerId as a follower of Author with id === userId
		var followerId = followRequest.data.actor.id;
		const firstName = followRequest.data.summary.split(" ")[0];
		var response = await axios.put(`${userId}/followers/${followerId}`);
		console.log(response);
		if (response.status !== 200) {
			// skip DELETE if PUT fails
			return;
		}
		// delete the accepted follow request
		var response = await axios.delete(`${userId}/inbox/${followRequest.id}`);
		console.log(response);
		setFollowRequests(followRequests.filter((e) => e != followRequest));
		NotificationBar.getInstance().addNotification(
			`${firstName} successfully added as a follower!`,
			NotificationBar.NT_SUCCESS
		);
	}

	async function handleRejectButton(followRequest) {
		var response = await axios.delete(`${userId}/inbox/${followRequest.id}`);
		console.log(response);
		if (response.status === 200) {
			setFollowRequests(followRequests.filter((e) => e != followRequest));
			NotificationBar.getInstance().addNotification(`Follow request deleted successfully.`, NotificationBar.NT_SUCCESS);
		}
	}

	// prompt loader until followRequests are set
	return !isLoaded ? (
		<Loader />
	) : (
		<Box sx={{ flexGrow: 1 }}>
			<Grid container spacing={0}></Grid>
			<Grid container spacing={5}>
				<Grid item xs={12} md={0}>
					<Demo>
						<List dense={dense}>
							{followRequests.map((followRequest) => (
								<ListItem
									secondaryAction={
										<Stack spacing={0.5} direction="row">
											<Button variant="outlined" onClick={() => handleAcceptButton(followRequest)}>
												Accept
											</Button>
											<Button variant="outlined" onClick={() => handleRejectButton(followRequest)}>
												Reject
											</Button>
										</Stack>
									}
								>
									<ListItemAvatar>
										<Avatar alt="actor" src={followRequest.data.actor.profileImage}></Avatar>
									</ListItemAvatar>
									<ListItemText primary={followRequest.data.summary} key={followRequest.data.actor.id} />
								</ListItem>
							))}
						</List>
					</Demo>
				</Grid>
			</Grid>
		</Box>
	);
}
