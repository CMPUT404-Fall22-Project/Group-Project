export default class PostListProvider {
	constructor(innerProvider, pageSize = 5) {
		this._provider = innerProvider;
		this._currentLoad = 0;
		this._pageSize = pageSize;
		this._pending = false;
		this._callbacks = [];
		this._posts = [];
	}

	listen(callback) {
		this._callbacks.push(callback);
	}

	_notify(data) {
		for (const callback of this._callbacks) {
			callback(data);
		}
	}

	_parseResult(request) {
		const data = request.data;
	}

	_saveResult(parsedData) {
		this._posts.push(parsedData);
		this._pending = false;
		return parsedData;
	}

	isDataRequested() {
		return this._pending;
	}

	requestData() {
		if (this._pending) {
			return null;
		}
		this._pending = true;
		const promise = this._provider
			.getPosts(Math.round(this._currentLoad / this._pageSize), this._pageSize)
			.then(this._parseResult.bind(this))
			.then(this._saveResult.bind(this))
			.then(this._notify.bind(this));
		this._currentLoad += this._pageSize;
		return promise;
	}

	getNumPosts() {
		return this._posts.length;
	}

	getPosts() {
		return [...this._posts];
	}
}

export class AbstractPostProvider {
	getPosts(pageIndex, count) {
		throw new Error("Not implemented");
	}
}
