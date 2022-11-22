import axios from "axios";
import Cookies from "universal-cookie";
import Author from "../data/containers/author";

const cookies = new Cookies();

export default class Authentication {
	/** @type {Authentication} */
	static _instance = null;
	static ID_COOKIE_TOKEN = "user_session";
	static ID_COOKIE_AUTHOR = "author_info";

	static getInstance() {
		if (!Authentication._instance) {
			Authentication._instance = new Authentication();
		}
		return Authentication._instance;
	}

	constructor() {
		this._isLoggedIn = false;
		this._sessionToken = cookies.get(Authentication.ID_COOKIE_TOKEN) || null;
		this._userData = cookies.get(Authentication.ID_COOKIE_AUTHOR) || null;
		if (this._userData) {
			this._userData = Author.parseDatabase(this._userData);
			this._isLoggedIn = this._sessionToken !== null;
		}

		this._authListeners = [];
	}

	isLoggedIn() {
		return this._isLoggedIn;
	}

	loggedInOrError() {
		if (!this.isLoggedIn()) {
			throw new Error("Not logged in");
		}
	}

	/**
	 * Gets the user data, or thorws an exception if you are not logged in
	 * @returns {Author}
	 */
	getUser() {
		this.loggedInOrError();
		return this._userData;
	}

	/**
	 * Gets the user data or the guest profile if not logged in
	 * @returns {Author}
	 */
	getUserSafe() {
		return this._userData || Author.guest();
	}

	addAuthChangedListener(listener) {
		this._authListeners.push(listener);
		return listener;
	}

	removeAuthChangedListener(listener) {
		const index = this._authListeners.indexOf(listener);
		if (index === -1) {
			throw new Error("Cannot remove authentication listener that was not added.");
		}
		this._authListeners.splice(index, 1);
	}

	/**
	 * Notifies all listeners that data about the profile or other auth data
	 * (not related to being logged in) has been updated somewhere in the app
	 */
	notifyAuthDataChanged() {
		axios({ method: "get", url: this._userData.getId() }).then((resp) => {
			this._setAuthor(resp.data);
		});
	}

	_notifyAuthChangedListeners(loggedIn) {
		for (const listener of this._authListeners) {
			listener(loggedIn);
		}
	}

	_sessionExists() {
		return this._sessionToken !== null;
	}

	_setAuthor(data) {
		cookies.set(Authentication.ID_COOKIE_AUTHOR, data);
		this._userData = Author.parseDatabase(data);
		this._notifyAuthChangedListeners(true);
	}

	authenticate(username, password) {
		if (!this) {
			// shorthand to let people reference this method directly
			return Authentication.getInstance().authenticate(username, password);
		}

		if (this._sessionExists()) {
			return new Promise((resolve, reject) => {
				this._notifyAuthChangedListeners(true); // nothing changed, but notify anyway
				resolve();
			});
		}

		return new Promise((resolve, reject) => {
			axios({
				method: "post",
				url: process.env.REACT_APP_HOST + "sessions/new/",
				// https://stackoverflow.com/a/37707074
				// headers: {
				// 	Authorization: "basic " + btoa(username) + ":" + btoa(password),
				// }, // django is being pain right now.
				data: {
					username: username,
					password: password,
				},
			})
				.then((resp) => {
					const data = resp.data;
					this._sessionToken = data.token;
					this._isLoggedIn = true;
					this._setAuthor(data.author);
					resolve();
				})
				.catch((request) => {
					reject(request);
				});
		});
	}

	logout() {
		var promise = axios({
			method: "post",
			url: process.env.REACT_APP_HOST + `sessions/end/`,
			data: {
				session: this._sessionToken,
			},
		});
		return promise.then(this.flushSession.bind(this));
	}

	flushSession() {
		this._isLoggedIn = false;
		this._sessionToken = null;
		this._userData = null;
		cookies.remove(Authentication.ID_COOKIE_TOKEN);
		cookies.remove(Authentication.ID_COOKIE_AUTHOR);
		this._notifyAuthChangedListeners(false);
	}

	getSessionToken() {
		this.loggedInOrError();
		return this._sessionToken;
	}
}
