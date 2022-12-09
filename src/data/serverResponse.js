import React from "react";
import NotificationBar from "../global/centralNotificationBar";

export default function preProcessAxios(axiosCall, useCustomHandler = false) {
	return new Promise((resolve, reject) => {
		// doesn't respect axios validateStatus arg.
		axiosCall
			.then((response) => {
				if (!response) {
					resolve();
					return;
				}
				resolve(response);
			})
			.catch((error) => {
				if (useCustomHandler) {
					reject(error);
					return;
				}
				reject(error);
				if (error.response) {
					// Request made and server responded
					const msg = handleHttpError(error);
					if (msg === null) {
						return;
					}

					const status = String(error.response.status);
					const text = String(error.response.statusText);

					var showMsg = "Unknown";
					if (text && status) {
						showMsg = status + " / " + text;
					} else if (text) {
						showMsg = text;
					} else if (status) {
						showMsg = "HTTP " + status;
					}

					var err = (
						<div>
							Error ({showMsg}): {msg}
						</div>
					);
					NotificationBar.getInstance().addNotification(err, NotificationBar.NT_ERROR, 1e10);
				} else if (error.request) {
					// The request was made but no response was received
					NotificationBar.getInstance().addNotification(
						"No Response From Server: " + String(error.request),
						NotificationBar.NT_ERROR,
						1e10
					);
				} else {
					// Something happened in setting up the request that triggered an Error
					NotificationBar.getInstance().addNotification(
						"Application Error: " + String(error.message),
						NotificationBar.NT_ERROR,
						1e10
					);
				}
			});
	});
}

function handleHttpError(error) {
	const errMsg = String(error.response.data.detail || error.response.data);
	if (NotificationBar.getInstance().anyNotificationMatches(errMsg)) {
		return null;
	}

	return errMsg;
}
