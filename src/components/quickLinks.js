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

// Enables user to navigate another Author's page via search
// Select component is auto-filled with the names of all authorized authors

export default function QuickLinks() {
	const [anchorEl, setAnchorEl] = useState();

	const handleClose = () => {
		setAnchorEl(null);
	};

	const handleButtonClick = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const viewLink = (link) => {
		history.push({ pathname: link });
		handleClose();
	};

	return (
		<div>
			<IconButton aria-label="Options" title="Goto..." onClick={handleButtonClick}>
				<MoreVertOutlinedIcon />
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
				<MenuItem onClick={viewLink.bind(this, "/posts/all/")}>Public Posts</MenuItem>
				<MenuItem onClick={viewLink.bind(this, "/inbox/")}>My Inbox</MenuItem>
				<MenuItem onClick={viewLink.bind(this, "/")}>My Posts</MenuItem>
			</Menu>
		</div>
	);
}
