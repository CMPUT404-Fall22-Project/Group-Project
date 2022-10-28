import React from "react";
import AbstractModalProvider, { ModalActions } from "./modalProvider";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";
import { withStyles } from "@mui/styles";
import ModalSystem from "../../global/modalSystem";
import { Button, Typography } from "@mui/material";

const ThemedButton = withStyles((theme) => ({
	root: {
		color: "#ffffff",
		backgroundColor: "#295d3a",
		fontWeight: "100",
		fontSize: "1rem",
		"&:hover": {
			backgroundColor: "#225232",
		},
	},
}))(Button);

export default class ModalTemplates {
	constructor() {
		throw new Error("Cannot create a static class.");
	}

	static RESULT_CANCELLED = 0;
	static RESULT_SUCCESS = 1;

	static notification(title, message) {
		const id = "NotificationModal" + String(Math.round(Math.random() * 10000));
		return new Promise((resolve, reject) => {
			const provider = new ModalNotificationProvider(title, message, resolve);
			ModalSystem.getInstance().addModal(id, provider, {
				centered: true,
				dialog: true,
				draggable: false,
				initialHeight: "auto",
				resizable: false,
			});
		});
	}

	static confirm(title, message) {
		const id = "ConfirmModal" + String(Math.round(Math.random() * 10000));
		return new Promise((resolve, reject) => {
			const provider = new ModalConfirmProvider(title, message, resolve);
			ModalSystem.getInstance().addModal(id, provider, {
				centered: true,
				dialog: true,
				draggable: false,
				initialHeight: "auto",
				resizable: false,
				initialWidth: "30em",
			});
		});
	}
}

class ModalNotificationProvider extends AbstractModalProvider {
	constructor(title, message, onClose = undefined) {
		super();
		this._title = title;
		this._message = message;
		this._onClose = onClose;
	}

	getTitle() {
		return this.createTitleWithIcon(InfoOutlinedIcon, this._title);
	}

	getHeader() {
		return <div></div>;
	}

	sendClose(action) {
		this.dispatchAction(ModalActions.EXECUTE_CLOSE);
		if (this._onClose) {
			this._onClose(action);
		}
	}

	getContent() {
		return (
			<div>
				<Typography style={{ padding: "1em" }} align="center">
					{this._message}
				</Typography>

				<ThemedButton
					style={{ display: "flex", margin: "auto", marginBottom: "1em", maxWidth: "50%" }}
					onClick={this.sendClose.bind(this, ModalTemplates.RESULT_SUCCESS)}
				>
					OK
				</ThemedButton>
			</div>
		);
	}
}

class ModalConfirmProvider extends AbstractModalProvider {
	constructor(title, message, onClose = undefined) {
		super();
		this._title = title;
		this._message = message;
		this._onClose = onClose;
	}

	getTitle() {
		return this.createTitleWithIcon(HelpOutlineOutlinedIcon, this._title);
	}

	getHeader() {
		return <div></div>;
	}

	sendClose(action) {
		this.dispatchAction(ModalActions.EXECUTE_CLOSE);
		if (this._onClose) {
			this._onClose(action);
		}
	}

	getContent() {
		return (
			<div>
				<div style={{ padding: "1em" }} align="center">
					{this._message}
				</div>
				<div
					style={{
						display: "flex",
						margin: "auto",
						marginTop: "1em",
						marginBottom: "1em",
						maxWidth: "100%",
						justifyContent: "space-evenly",
						marginLeft: "50%",
					}}
				>
					<ThemedButton style={{ width: "6em" }} onClick={this.sendClose.bind(this, ModalTemplates.RESULT_SUCCESS)}>
						OK
					</ThemedButton>
					<ThemedButton style={{ width: "6em" }} onClick={this.sendClose.bind(this, ModalTemplates.RESULT_CANCELLED)}>
						CANCEL
					</ThemedButton>
				</div>
			</div>
		);
	}
}
