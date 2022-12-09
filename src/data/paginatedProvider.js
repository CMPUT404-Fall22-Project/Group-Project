import { proxiedAxios } from "../utils/proxy";

export default class PaginatedProvider {
	constructor(innerProvider, arrayName = "items", pageSize = 5) {
		this._provider = innerProvider;
		this._currentLoad = 0;
		this._pageSize = pageSize;
		this._pending = false;
		this._arrayName = arrayName;
		this._callbacks = [];
		this._data = [];
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
		this._data.push(inputData);
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
			.then((resp) => resp.data[this._arrayName])
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
		return this._data.length;
	}

	getData() {
		return [...this._data];
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
		return proxiedAxios({
			method: "get",
			url: this._dataUrl,
			params: {
				page: pageIndex,
				size: count,
			},
		});
	}
}
