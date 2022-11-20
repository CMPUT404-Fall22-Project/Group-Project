import axios from "axios";
import React, { useEffect, useState } from "react";
import { Button, MenuItem } from "@mui/material";
import "./followRequests.css";
import Box from "@mui/material/Box";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import List from "@mui/material/List";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import { styled } from "@mui/material/styles";
import Authentication from "../global/authentication";
import Loader from "../components/loader";
import AbstractModalProvider from "./modals/modalProvider";
import ModalSystem from "../global/modalSystem";
import AccountBoxOutlinedIcon from "@mui/icons-material/AccountBoxOutlined";
import NotificationBar from "../global/centralNotificationBar";

const Demo = styled("div")(({ theme }) => ({
	backgroundColor: theme.palette.background.paper,
}));

export const FollowRequestsButton = () => {
	const [clicked, setClicked] = useState(false);
	return (
		<div>
			<Button
				variant="contained"
				onClick={() => {
					setClicked(!clicked);
				}}
			>
				Follow Requests
			</Button>
			<FollowRequestsToggle open={clicked}></FollowRequestsToggle>
		</div>
	);
};

export const FollowRequestsMenuItem = ({ onClick, ...props }) => {
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

export const FollowRequestsToggle = ({ open }) => {
	if (open) {
		return <TopAppBar />;
	}
	return null;
};
export function TopAppBar() {
	return (
		<div style={{ width: "50%", height: "100%", position: "absolute" }}>
			<Box sx={{ flexGrow: 1, maxWidth: 1000 }}>
				<div style={{ width: "100%", height: "100%", position: "absolute", overflow: "auto" }}>
					<FollowRequests></FollowRequests>
				</div>
			</Box>
		</div>
	);
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
		const followerId = followRequest.data.actor.id;
		const firstName = followRequest.data.summary.split(" ")[0];
		axios
			.put(`${userId}/followers/${followerId}`)
			.then((res) => {
				console.log(res);
				NotificationBar.getInstance().addNotification(
					`${firstName} successfully added as a follower!`,
					NotificationBar.NT_SUCCESS
				);
			})
			.catch((err) => console.log(err));
		axios
			.delete(`${userId}/inbox/${followRequest.id}`)
			.then((res) => {
				console.log(res);
			})
			.catch((err) => console.log(err));
	}

	async function handleRejectButton(followRequest) {
		axios
			.delete(`${userId}/inbox/${followRequest.id}`)
			.then((res) => {
				console.log(res);
				NotificationBar.getInstance().addNotification(
					`Follow request deleted successfully.`,
					NotificationBar.NT_SUCCESS
				);
			})
			.catch((err) => console.log(err));
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
