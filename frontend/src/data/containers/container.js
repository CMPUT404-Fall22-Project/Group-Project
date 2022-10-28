export default class DataContainer {
	static validateTypeof = (data, type) => {
		if (type !== data.type) {
			throw new Error(`Type mismatch: Tried to load ${data.type} into ${type}`);
		}
	};

	static parseDatabase(data) {
		throw new Error("Not implemented");
	}

	encodeDatabase() {
		throw new Error("Not implemented");
	}
}
