import React, { useState, useEffect } from "react";
import axios from "axios";
import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import Authentication from "../global/authentication";
import { Autocomplete, TextField, Grid, IconButton } from "@mui/material";
import NotificationBar from "../global/centralNotificationBar";
import SendOutlinedIcon from "@mui/icons-material/SendOutlined";

// Enables an Author to submit a Follow Request to another Author
// Select component is auto-filled with the names of all authorized authors
// Selection of an author enables the "Submit Follow Request" button
// Clicking the "Submit Follow Request" sends a POST request to the inbox of the selected Author

export default function FollowRequestSearch() {
	const [authorId, setAuthorId] = useState("");
	const [authors, setAuthors] = useState([]);
	const userId = Authentication.getInstance().getUser().getId();

	useEffect(() => {
		handleAuthors();
	}, []);

	const handleAuthors = async () => {
		// gets all of the authors
		// gets all of the users the author is following
		// generates a list of all authors - the logged in author - authors the author is already following

		// Get all of the authors
		var response = await axios.get(process.env.REACT_APP_HOST + `authors/`);
		console.log(response);
		const authors = response.data.items;

		// get all authors that the logged in user is following
		response = await axios.get(process.env.REACT_APP_HOST + `authors/${userId}/following/`);
		console.log(response);
		const following = response.data.items;
		const followingIds = [];
		for (let f of following) {
			followingIds.push(f.id);
		}
		const arr = [];
		for (let a of authors) {
			// only fill arr with authors that the author is not currently following
			if (a.id !== userId && !followingIds.includes(a.id)) {
				arr.push({ label: a.displayName, id: a.id });
			}
			setAuthors(arr);
			console.log("final arr", arr);
		}
	};

	const handleButtonClick = (event) => {
		// Send a follow Request to the selected authorId's inbox
		axios
			.post(process.env.REACT_APP_HOST + `authors/${authorId}/inbox/`, { id: authorId })
			.then((res) => {
				NotificationBar.getInstance().addNotification("Follow request sent successfully!", NotificationBar.NT_SUCCESS);
			})
			.catch((err) => NotificationBar.getInstance().addNotification(err, NotificationBar.NT_ERROR));
	};

	return (
		<Box sx={{ minWidth: 120 }}>
			<FormControl fullWidth style={{ display: "flex", flexDirection: "row" }}>
				<Autocomplete
					onChange={(event, author) => {
						setAuthorId(author.id);
					}}
					freeSolo
					id="free-solo-2-demo"
					disableClearable
					options={authors}
					style={{
						margin: "0.25em",
						width: "25em",
					}}
					size="small"
					renderInput={(params) => (
						<TextField
							{...params}
							style={{
								background: "#ffffffff",
							}}
							variant="standard"
							label="Search Authors"
							InputProps={{
								...params.InputProps,
								type: "search",
							}}
						/>
					)}
				/>
				<IconButton
					aria-label="Send"
					title="Send Follow Request"
					disabled={!authorId}
					onClick={() => {
						handleButtonClick();
					}}
				>
					<SendOutlinedIcon />
				</IconButton>
			</FormControl>
		</Box>
	);
}
