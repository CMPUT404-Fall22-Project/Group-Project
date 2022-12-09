import DataContainer from "./container";

export default class GithubEvent extends DataContainer {
	static TYPE = "author";

	constructor(title, message, published, authorInfo) {
		super();
		this._title = title;
		this._message = message;
		this._published = published;
		this._authorInfo = authorInfo;
	}

	getTitle() {
		return this._title;
	}

	getMessage() {
		return this._message;
	}

	getPublished() {
		return this._published;
	}

	getAuthorInfo() {
		return this._authorInfo;
	}

	static parseDatabase(data) {
		const title = data.type;
		var message = "Unknown event.";
		console.log(data);
		switch (title) {
			case "PushEvent":
				message =
					"Pushed to branch " +
					data.payload.ref +
					" @ " +
					data.repo.name +
					".\n\nCommits:\n\n" +
					data.payload.commits.map((x) => "**" + x.sha.substring(0, 8) + "**   " + x.message).join("\n\n");
				break;
			case "PullRequestEvent":
				message = "Pull request for  " + data.repo.name + ".\n\nStatus: " + data.payload.action;
				break;
			case "CreateEvent":
				message = "Created a new branch on " + data.repo.name + ".\n\nName: " + data.payload.ref;
				break;
			case "ForkEvent":
				message = "Forked " + data.repo.name;
				break;

			default:
				break;
		}
		return new GithubEvent(title, message, new Date(data.created_at), data.actor);
	}
}
