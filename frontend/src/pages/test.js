import axios from "axios";
import React, { Component, useEffect, useState } from "react";
import { Button } from "@mui/material";
import "./test.css";
import background from "../static/back.webp";
import Box from "@mui/material/Box";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import List from "@mui/material/List";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import DeleteIcon from "@mui/icons-material/Delete";
import Stack from "@mui/material/Stack";
import { styled } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import { LikeButton } from "../components/likeButton";
import Authentication from "../global/authentication";
import Loader from "../components/loader";

const Demo = styled("div")(({ theme }) => ({
	backgroundColor: theme.palette.background.paper,
}));

export function TopAppBar() {
	return (
		<div style={{ width: "50%", height: "100%", position: "absolute" }}>
			<Box sx={{ flexGrow: 1, maxWidth: 1000 }}>
				<AppBar position="static">
					<Toolbar>
						{/* <IconButton size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
							<MenuIcon />
						</IconButton> */}
						<Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
							Follow Requests
						</Typography>
					</Toolbar>
				</AppBar>
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
		response = await axios.get(process.env.REACT_APP_HOST + `authors/${userId}/followers/`);
		console.log(response);
		const followerIds = [];
		for (let follower of response.data.items) {
			followerIds.push(follower.id);
		}
		setFollowerIds(followerIds);
		// Get all follow requests
		var response = await axios.get(process.env.REACT_APP_HOST + `authors/${userId}/inbox/`);
		console.log(response);
		const followRequests = [];
		for (let item of response.data.items) {
			if (item.dataType === "Follow") {
				const id = item.data.actor.id;
				// Don't add follow requests from authors already following this author
				if (!followerIds.includes(id)) {
					followRequests.push(item.data);
				}
			}
		}
		setFollowRequests(followRequests);
		setIsLoaded(true);
	};

	async function handleAcceptButton(followRequest) {
		// PUT the Author with id === followerId as a follower of Author with id === userId
		const followerId = followRequest.actor.id;
		const firstName = followRequest.summary.split(" ")[0];
		axios
			.put(process.env.REACT_APP_HOST + `authors/${userId}/followers/${followerId}`)
			.then((res) => {
				console.log(res);
				alert(`${firstName} successfully added as a follower!`);
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
											<Button variant="outlined">Reject</Button>
										</Stack>
									}
								>
									<ListItemAvatar>
										<Avatar alt="actor" src={followRequest.actor.profileImage}></Avatar>
									</ListItemAvatar>
									<ListItemText primary={followRequest.summary} key={followRequest.actor.id} />
								</ListItem>
							))}
						</List>
					</Demo>
				</Grid>
			</Grid>
		</Box>
	);
}

class LoginComponent extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {}

	login() {}

	render() {
		return (
			<div
				className="Fade-In"
				style={{
					backgroundImage: `url(${background})`,
					backgroundRepeat: "no-repeat",
					backgroundSize: "cover",
					top: "0",
					height: "100%",
					width: "100%",
					position: "absolute",
					overflow: "clip",
				}}
			>
				<div style={{ height: "50%", minHeight: "1250px", position: "relative" }}>
					<LikeButton className="like-button-wrapper">Like</LikeButton>
					<div className="outer-login-box">
						<div classname="follower-requests">
							<TopAppBar classname="top-app-bar"></TopAppBar>
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default LoginComponent;
