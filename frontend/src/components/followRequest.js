import React, { useState, useEffect } from "react";
import axios from "axios";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Button from "@mui/material/Button";

// Enables an Author to submit a Follow Request to another Author
// Select component is auto-filled with the names of all authorized authors
// Selection of an author enables the "Submit Follow Request" button
// Clicking the "Submit Follow Request" sends a POST request to the inbox of the selected Author

export default function FollowRequest() {
	const [author, setAuthor] = useState("");
	const [authors, setAuthors] = useState([]);

	useEffect(() => {
		axios
			.get(`http://127.0.0.1:8000/authors/`)
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
			arr.push(
				<MenuItem key={a.id} value={a.id}>
					{a.displayName}
				</MenuItem>
			);
		}
		setAuthors(arr);
	};

	const handleSelectChange = (event) => {
		setAuthor(event.target.value);
	};

	const handleButtonClick = (event) => {
		// Send a follow Request to the selected author
		const id = "WRYvjKiZj8Ar4V6REbTQRZWhwOlYuoVb";
		axios
			.post(`http://127.0.0.1:8000/authors/${id}/inbox/`, { id: "WRYvjKiZj8Ar4V6REbTQRZWhwOlYuoVb" })
			.then((res) => console.log(res))
			.catch((err) => console.log(err));
	};

	return (
		<Box sx={{ minWidth: 120 }}>
			<FormControl fullWidth>
				<InputLabel id="demo-simple-select-label">Select an Author</InputLabel>
				<Select
					labelId="demo-simple-select-label"
					id="demo-simple-select"
					value={author}
					label="Author"
					onChange={handleSelectChange}
				>
					{authors}
				</Select>
				<Button
					variant="contained"
					disabled={!author}
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
