import * as React from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardActions from "@mui/material/CardActions";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import GitHubIcon from "@mui/icons-material/GitHub";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import axios from "axios";

// https://mui.com/material-ui/react-card/, Material UI, 2022-10-27
// TODO: add follow functionality
// TODO: change follow icon when you are following them
// TODO: change axios request to allow follow requests?
const author = (props) => {
	// do we show id/url/host?
	const { author_id, displayName, github, profileImage, id } = props;

	const followData = { id };

	const handleFollow = (e) => {
		axios({
			method: "post",
			url: "service/authors/" + displayName + "/inbox",
			data: followData,
		})
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return (
		<Card sx={{ maxWidth: 345 }}>
			<CardHeader
				avatar={<Avatar alt="Profile Picture" src={profileImage}></Avatar>} // make sure pfp is in the right format (needs link?)
				title={displayName}
				subheader={author_id}
			/>
			<CardActions disableSpacing>
				<IconButton aria-label="Follow" onClick={handleFollow}>
					<PersonAddIcon />
				</IconButton>
				<IconButton aria-label="GitHub" href={github}>
					<GitHubIcon />
				</IconButton>
			</CardActions>
		</Card>
	);
};

export default author;
