import React from "react";

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
