import React from "react";
import { Typography } from "@mui/material";

export function iconText(text, icon, padding = "0.5em", iconSize = "medium", overrideStyles = {}) {
	return (
		<span
			style={{
				display: "flex",
				alignItems: "center",
				flexWrap: "nowrap",
				justifyContent: "center",
				width: "100%",
				wordBreak: "break-word",
				...overrideStyles,
			}}
		>
			{React.createElement(icon, {
				style: {
					marginRight: padding,
				},
				fontSize: iconSize,
			})}
			{text}
		</span>
	);
}

export function renderPublishDate(date) {
	const d = new Date(date);
	return (
		<Typography variant="caption">
			<i>Published at {d.toLocaleDateString() + " - " + d.toLocaleTimeString()}</i>
		</Typography>
	);
}
