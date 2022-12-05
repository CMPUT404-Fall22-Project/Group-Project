import * as React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";
import history from "../history";

// https://mui.com/material-ui/react-menu/
// https://stackoverflow.com/a/69910433
const options = ["Public Posts", "My Inbox", "My Posts"];

export default function ViewPostTypes() {
	const [anchorEl, setAnchorEl] = React.useState(null);
	const [selectedIndex, setSelectedIndex] = React.useState(1);
	const open = Boolean(anchorEl);
	const handleClickListItem = (event) => {
		setAnchorEl(event.currentTarget);
	};

	const handleMenuItemClick = (event, index) => {
		setSelectedIndex(index);
		setAnchorEl(null);
		if (index === 0) {
			history.push({ pathname: "/posts/all/" });
		} else if (index === 1) {
			history.push({ pathname: "/inbox/" });
		} else if (index === 2) {
			history.push({ pathname: "/" });
		}
	};

	const handleClose = () => {
		setAnchorEl(null);
	};

	return (
		<div>
			<List component="nav" aria-label="Device settings" style={{ margin: 10 }}>
				<ListItem
					button
					id="lock-button"
					aria-haspopup="listbox"
					aria-controls="lock-menu"
					aria-expanded={open ? "true" : undefined}
					onClick={handleClickListItem}
				>
					<ListItemText
						primaryTypographyProps={{
							color: "white",
						}}
						primary={options[selectedIndex]}
					/>
				</ListItem>
			</List>
			<Menu
				id="lock-menu"
				anchorEl={anchorEl}
				open={open}
				onClose={handleClose}
				MenuListProps={{
					"aria-labelledby": "lock-button",
					role: "listbox",
				}}
			>
				{options.map((option, index) => (
					<MenuItem
						key={option}
						selected={index === selectedIndex}
						onClick={(event) => handleMenuItemClick(event, index)}
					>
						{option}
					</MenuItem>
				))}
			</Menu>
		</div>
	);
}
