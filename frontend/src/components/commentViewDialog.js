import React, { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { IconButton } from "@mui/material";
import CommentIcon from "@mui/icons-material/Comment";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import CommentsListDialog from "./commentsListDialog";

const ScrollDialog = (props) => {
	const { baseURL } = props;

	const [open, setOpen] = React.useState(false);
	const [scroll, setScroll] = React.useState("paper");

	const handleClickOpen = (scrollType) => () => {
		setOpen(true);
		setScroll(scrollType);
	};

	const handleClose = () => {
		setOpen(false);
	};

	const descriptionElementRef = React.useRef(null);
	React.useEffect(() => {
		if (open) {
			const { current: descriptionElement } = descriptionElementRef;
			if (descriptionElement !== null) {
				descriptionElement.focus();
			}
		}
	}, [open]);

	return (
		<span>
			<IconButton aria-label="Comment" title="Comment on above post" onClick={handleClickOpen("body")}>
				<CommentIcon />
			</IconButton>
			<Dialog
				open={open}
				onClose={handleClose}
				scroll={scroll}
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
			>
				<DialogTitle id="scroll-dialog-title">Comments</DialogTitle>
				<DialogContent dividers={scroll === "body"} id="commentList">
					<Box sx={{ width: "100%", bgcolor: "background.paper" }}>
						<nav aria-label="main mailbox folders">
							<List>
								<CommentsListDialog baseURL={baseURL}></CommentsListDialog>
							</List>
						</nav>
					</Box>
				</DialogContent>
			</Dialog>
		</span>
	);
};

export default ScrollDialog;
