import React, { useState, useEffect } from "react";
import axios from "axios";
import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import Authentication from "../global/authentication";
import { Autocomplete, TextField, Grid, IconButton, Menu, MenuItem } from "@mui/material";
import NotificationBar from "../global/centralNotificationBar";
import SendOutlinedIcon from "@mui/icons-material/SendOutlined";
import MoreVertOutlinedIcon from "@mui/icons-material/MoreVertOutlined";
import history from "../history";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
// Enables user to navigate another Author's page via search
// Select component is auto-filled with the names of all authorized authors

export default function AuthorSearch() {
	const [authorId, setAuthorId] = useState("");
	const [authors, setAuthors] = useState([]);
	const [autoCompleteAuthors, setAutoCompleteAuthors] = useState([]);
	const userId = Authentication.getInstance().getUser().getId();

	const [anchorEl, setAnchorEl] = useState();

	const handleClose = () => {
		setAnchorEl(null);
	};

	useEffect(() => {
		handleAuthors();
	}, []);

	const handleAuthors = async () => {
		// Get all of the authors across all nodes
		var response = await axios.get(process.env.REACT_APP_HOST + `authors/all/`);
		const authors = response.data.items;
		var arr = [];
		for (const a of authors) {
			if (!a.displayName || !a.id) {
				console.error("Bad API response: missing displayName or id " + JSON.stringify(a));
				continue;
			}
			arr.push({ label: a.displayName, id: a.id });
		}
		// Remove the logged in author from arr
		arr = arr.filter((a) => a.id !== userId);
		setAutoCompleteAuthors(arr);
		setAuthors(authors);
	};

	const handleButtonClick = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const viewProfile = () => {
		const author = authors.find((e) => e.id == authorId);
		history.push({ pathname: "/authors/" + authorId.split("/authors/")[1], state: { author: author } });
		handleClose();
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
					options={autoCompleteAuthors}
					getOptionLabel={(x) => x.label}
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
							sx={{
								paddingLeft: "0.25em",
							}}
						/>
					)}
				/>
				<IconButton aria-label="Options" title="See Options" disabled={!authorId} onClick={handleButtonClick}>
					<ExpandMoreIcon style={{ color: "white" }} />
				</IconButton>
				<Menu
					id="long-menu"
					MenuListProps={{
						"aria-labelledby": "long-button",
					}}
					anchorEl={anchorEl}
					open={Boolean(anchorEl)}
					onClose={handleClose}
				>
					<MenuItem onClick={viewProfile}>View Profile</MenuItem>
				</Menu>
			</FormControl>
		</Box>
	);
}
