import axios from "axios";
import React, { useState, useEffect } from "react";
import { Octokit } from "octokit";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";

export default function GithubEvents() {
	const [events, setEvents] = useState([]);

	const octokit = new Octokit({
		auth: process.env.GIT,
		userAgent: "aaronskiba",
	});
	useEffect(() => {
		getGithubEvents();
	}, []);

	async function getGithubEvents() {
		var response = await octokit.request("GET https://api.github.com/users/aaronskiba/events");
		if (response.status == 200) {
			const events = [];
			for (let event of response.data) {
				events.push(event);
			}
			setEvents(events);
		}
	}
	return (
		<span>
			<ThumbUpIcon />
		</span>
	);
}
