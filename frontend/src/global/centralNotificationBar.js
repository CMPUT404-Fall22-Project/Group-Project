import React, { Component } from "react";
import { Collapse, Paper, Alert } from "@mui/material";
import { stringifyComponent } from "../utils/stringify";

export default class NotificationBar extends Component {
	/** @type {NotificationBar} */
	static _instance = null;

	static NT_SUCCESS = "success";
	static NT_INFO = "info";
	static NT_WARNING = "warning";
	static NT_ERROR = "error";

	constructor(props) {
		super(props);

		this.state = {
			notifications: [],
			id: 0,
			mounted: false,
		};
		NotificationBar._instance = this;
	}

	componentDidMount() {
		this.setState({ mounted: true });
	}

	componentWillUnmount() {
		this.setState({ mounted: false });
	}

	static getInstance() {
		const inst = NotificationBar._instance;
		if (!inst.state.mounted) {
			throw new Error("Notification bar not mounted");
		}
		return inst;
	}

	addNotification(text, type, timeout = 5000) {
		this.setState(
			(prevState) => {
				const id = prevState.id;
				const timeoutId = setTimeout(() => {
					this.clearNofication(id);
				}, timeout);
				const notif = {
					message: text,
					type: type,
					id: id,
					open: false,
					opening: true,
					timeoutId: timeoutId,
				};
				return { notifications: [...prevState.notifications, notif], id: prevState.id + 1 }; // remove dead entries here.
			},
			() => {
				// lazy way to make the collapse go both ways
				var notifs = [...this.state.notifications];
				for (const x of notifs) {
					if (x.opening) {
						x.opening = false;
						x.open = true;
					}
				}
				this.setState({ notifications: notifs });
			}
		);
	}

	anyNotificationMatches(regex) {
		for (const notif of this.state.notifications) {
			if (notif.open && stringifyComponent(notif.message).match(regex)) {
				return true;
			}
		}
		return false;
	}

	clearNotificationsMatching(regex) {
		var anyFound = false;
		for (const notif of this.state.notifications) {
			if (notif.open && stringifyComponent(notif.message).match(regex)) {
				this.clearNofication(notif.id, notif.timeoutId);
				anyFound = true;
			}
		}
		return anyFound;
	}

	clearNofication(id, timeoutId = null) {
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
		}
		this.setState((prevState) => {
			var notifs = [...prevState.notifications].filter((x) => x.open);
			var target = notifs.find((x) => x.id === id);
			if (target) {
				target.open = false;
			} else {
				console.error("Cannot find notification with id " + String(id));
			}
			return { notifications: notifs };
		});
	}

	render() {
		const items = [...this.state.notifications];
		items.reverse();
		return (
			<div
				style={{
					marginLeft: "auto",
					marginRight: "auto",
					height: 0,
					zIndex: 1040,
				}}
			>
				{items.map((item) => (
					<Collapse in={item.open} key={item.id}>
						<Paper style={{ width: "40vw", margin: "0.25em" }}>
							<Alert onClose={this.clearNofication.bind(this, item.id, item.timeoutId)} severity={item.type}>
								{item.message}
							</Alert>
						</Paper>
					</Collapse>
				))}
			</div>
		);
	}
}
