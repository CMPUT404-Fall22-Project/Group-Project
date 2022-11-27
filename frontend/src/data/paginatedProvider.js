import axios from "axios";

export default class PaginatedProvider {
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

	_notify(success, data) {
		for (const callback of this._callbacks) {
			callback(success, data);
		}
	}

	_saveResult(inputData) {
		this._posts.push(inputData);
		this._pending = false;
		return inputData;
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
			.getData(Math.round(this._currentLoad / this._pageSize) + 1, this._pageSize)
			.then((resp) => resp.data.items)
			.then(this._saveResult.bind(this))
			.then((data) => {
				this._currentLoad += this._pageSize;
				return data;
			})
			.then(this._notify.bind(this, true))
			.catch((err) => {
				console.error(err);
				this._pending = false;
				this._notify(false, err);
			});

		return promise;
	}

	skip(count) {
		this._currentLoad += count;
		return this;
	}

	getNumData() {
		return this._posts.length;
	}

	getData() {
		return [...this._posts];
	}
}

export class AbstractElementProvider {
	getData(pageIndex, count) {
		throw new Error("Not implemented");
	}
}

export class GenericElementProvider extends AbstractElementProvider {
	constructor(dataUrl) {
		super();
		this._dataUrl = dataUrl;
	}

	getData(pageIndex, count) {
		return axios({
			method: "get",
			url: this._dataUrl,
			params: {
				page: pageIndex,
				size: count,
			},
		});
	}
}
