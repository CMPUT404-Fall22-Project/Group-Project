import React, { useState, useEffect } from "react";
import axios from "axios";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Button from "@mui/material/Button";
import Authentication from "../global/authentication";

// Enables an Author to submit a Follow Request to another Author
// Select component is auto-filled with the names of all authorized authors
// Selection of an author enables the "Submit Follow Request" button
// Clicking the "Submit Follow Request" sends a POST request to the inbox of the selected Author

export default function FollowRequest() {
	const [authorId, setAuthorId] = useState("");
	const [authors, setAuthors] = useState([]);
	const userId = Authentication.getInstance().getUser().getId();

	useEffect(() => {
		axios
			.get(process.env.REACT_APP_HOST + `authors/`)
			.then((res) => {
				console.log(res);
				handleAuthors(res.data.items);
			})
			.catch((err) => console.log(err));
	}, []);

	const handleAuthors = (authors) => {
		// Push the authors into an array of MenuItems
		// <MenuItem value={a.id}>{a.displayName}</MenuItem>
		const arr = [];
		for (let a of authors) {
			// prevents author from sending follow request to self
			if (a.id !== userId) {
				arr.push(
					<MenuItem key={a.id} value={a.id}>
						{a.displayName}
					</MenuItem>
				);
			}
			setAuthors(arr);
		}
	};

	const handleSelectChange = (event) => {
		setAuthorId(event.target.value);
	};

	const handleButtonClick = (event) => {
		// Send a follow Request to the selected authorId's inbox
		axios
			.post(`http://127.0.0.1:8000/authors/${authorId}/inbox/`, { id: userId })
			.then((res) => {
				console.log(res);
				alert("Follow request sent successfully!");
			})
			.catch((err) => console.log(err));
	};

	return (
		<Box sx={{ minWidth: 120 }}>
			<FormControl fullWidth>
				<InputLabel id="demo-simple-select-label">Select an Author</InputLabel>
				<Select
					labelId="demo-simple-select-label"
					id="demo-simple-select"
					value={authorId}
					label="Author"
					onChange={handleSelectChange}
				>
					{authors}
				</Select>
				<Button
					variant="contained"
					disabled={!authorId}
					onClick={() => {
						handleButtonClick();
					}}
				>
					Submit Follow Request
				</Button>
			</FormControl>
		</Box>
	);
}
