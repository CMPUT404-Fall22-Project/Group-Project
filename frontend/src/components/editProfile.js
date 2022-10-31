import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Grid, Button, TextField } from "@mui/material";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";

export default function EditProfile() {
	// Used main ideas from https://www.youtube.com/watch?v=GBbGEuZdyRg&list=PL1oBBulPlvs84AmRmT-_3dGz4KHYuINsj&index=18

	const userID = Authentication.getInstance().getUser().getId();
	const [author, setAuthor] = useState({
		displayName: "",
		github: "",
		profileImage: "",
	});
	const { displayName, github, profileImage } = author;

	useEffect(() => {
		const loadAuthor = async () => {
			const res = await axios.get(process.env.REACT_APP_HOST + `authors/${userID}`);
			setAuthor(res.data);
		};
		loadAuthor();
	}, []);

	const HandleAuthor = (auth) => {
		// Fill's text field with the author's stored data
		console.log(auth.target.name, ":", auth.target.value);
		setAuthor({ ...author, [auth.target.name]: auth.target.value });
	};

	const HandleSubmit = (e) => {
		// POSTs to author to update data
		axios
			.post(process.env.REACT_APP_HOST + `authors/${userID}`, author)
			.then((res) => NotificationBar.getInstance().addNotification("Edited successfully!", NotificationBar.NT_SUCCESS))
			.catch((err) => NotificationBar.getInstance().addNotification(err, NotificationBar.NT_ERROR));
	};

	return (
		<Box
			sx={{
				display: "flex",
				justifyContent: "center",
				alignItems: "center",
			}}
		>
			<Box component="form" onSubmit={HandleSubmit} sx={{ mt: 8 }}>
				<Grid container spacing={2}>
					<Grid item xs={10}>
						<TextField
							name="displayName"
							required
							fullWidth
							id="displayName"
							value={displayName}
							label="Display Name"
							onChange={(e) => HandleAuthor(e)}
						/>
					</Grid>
					<Grid item xs={10}>
						<TextField
							name="github"
							required
							fullWidth
							id="github"
							value={github}
							label="Github URL"
							onChange={(e) => HandleAuthor(e)}
						/>
					</Grid>
					<Grid item xs={10}>
						<TextField
							name="profileImage"
							required
							fullWidth
							id="profileImage"
							value={profileImage}
							label="Profile image"
							onChange={(e) => HandleAuthor(e)}
						/>
					</Grid>
					<Grid item xs={5}>
						<Button
							type="submit"
							variant="contained"
							sx={{ mb: 10 }}
							onClick={() => {
								HandleSubmit();
							}}
						>
							Submit
						</Button>
					</Grid>
				</Grid>
			</Box>
		</Box>
	);
}
