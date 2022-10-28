import Author from "./author";
import DataContainer from "./container";

export default class Post extends DataContainer {
	static TYPE = "post";

	// base data contains all top level info that is not an object
	constructor(baseData, author, comments) {
		super();
		this._baseData = baseData;
		if (author) {
			this._baseData.author = author;
		} else {
			this._baseData.author = Author.parseDatabase(this._baseData.author);
		}
		if (comments) {
			this._baseData.commentsSrc = comments;
		}
	}

	getAuthor() {
		return this._baseData.author;
	}

	setAuthor(author) {
		this._baseData.author = author;
	}

	getNumComments() {
		return this._baseData.count;
	}

	getNextComments() {
		// TODO
	}

	getComments() {
		return this._baseData.commentsSrc.comments;
	}

	getBaseData() {
		return this._baseData;
	}

	setBaseData(baseData) {
		this._baseData = baseData;
	}

	encodeDatabase() {
		const obj = {
			...this._baseData,
			author: this.getAuthor().encodeDatabase(),
			type: "post",
		};

		return obj;
	}

	static parseDatabase(data) {
		this.validateTypeof(data, Post.TYPE);
		return new Post(data);
	}
}
