import * as React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardActions from "@mui/material/CardActions";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import GitHubIcon from "@mui/icons-material/GitHub";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import axios from "axios";
import Authentication from "../global/authentication";
import { Typography } from "@mui/material";

// https://mui.com/material-ui/react-card/, Material UI, 2022-10-27
// TODO: add follow functionality
// TODO: change follow icon when you are following them
// TODO: change axios request to allow follow requests?
const AuthorCardComponenet = ({ data }) => {
	const handleFollow = (e) => {
		axios({
			method: "post",
			url: "authors/" + data.getId() + "/inbox",
			data: Authentication.getInstance().getUser().getId(),
		})
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return (
		<div style={{ display: "flex", justifyContent: "space-between" }}>
			<div style={{ display: "inherit" }}>
				<Avatar alt="Profile Picture" src={data.getProfileImageUrl()}></Avatar>

				<Typography style={{ marginLeft: "0.5em" }}>{data.getUsername()}</Typography>
			</div>
			<div>
				{/* <IconButton aria-label="Follow" title="Follow?" onClick={handleFollow}>
					<PersonAddIcon />
				</IconButton> */}
				<IconButton aria-label="GitHub" title="Github" href={data.getGithubUrl()}>
					<GitHubIcon />
				</IconButton>
			</div>
		</div>
	);
};

export default AuthorCardComponenet;
