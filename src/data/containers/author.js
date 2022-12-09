import DataContainer from "./container";

export default class Author extends DataContainer {
	static TYPE = "author";

	constructor(id, host, username, url, githubUrl, profileImage) {
		super();
		this._id = id;
		this._host = host;
		this._username = username;
		this._url = url;
		this._githubUrl = githubUrl;
		this._profileImageUrl = profileImage;
	}

	getId() {
		return this._id;
	}

	getHost() {
		return this._host;
	}

	getUsername() {
		return this._username;
	}

	getUrl() {
		return this._url;
	}

	getGithubUrl() {
		return this._githubUrl;
	}

	getProfileImageUrl() {
		return this._profileImageUrl;
	}

	setId(id) {
		this._id = id;
	}

	setHost(host) {
		this._host = host;
	}

	setUsername(username) {
		this._username = username;
	}

	setUrl(url) {
		this._url = url;
	}

	setGithubUrl(gitUrl) {
		this._githubUrl = gitUrl;
	}

	setProfileImageUrl(imageLink) {
		this._profileImageUrl = imageLink;
	}

	encodeDatabase() {
		const obj = {
			type: "author",
			id: this._id,
			host: this._host,
			displayName: this._username,
			url: this._url,
			github: this._githubUrl,
			profileImage: this._profileImageUrl,
		};

		return obj;
	}

	static parseDatabase(data) {
		this.validateTypeof(data, Author.TYPE);
		return new Author(data.id, data.host, data.displayName, data.id, data.github, data.profileImage);
	}

	static guest() {
		const host = process.env.REACT_APP_HOST;
		return new Author(null, host, "", null, null, null);
	}
}
