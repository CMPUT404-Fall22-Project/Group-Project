import Author from "./author";
import DataContainer from "./container";

export default class Comment extends DataContainer {
	static TYPE = "comment";

	constructor(id, author, comment, contentType, publishedAt) {
		super();
		this._id = id;
		this._author = author;
		this._comment = comment;
		this._contentType = contentType;
		this._publishedAt = publishedAt;
	}

	getId() {
		return this._id;
	}

	getAuthor() {
		return this._author;
	}

	getContent() {
		return this._comment;
	}

	getContentType() {
		return this._contentType;
	}

	getPublishedAt() {
		return this._publishedAt;
	}

	encodeDatabase() {
		const obj = {
			type: "comment",
			id: this._id,
			author: this._author.encodeDatabase(),
			comment: this._comment,
			contentType: this._contentType,
			published: this._publishedAt,
		};
		return obj;
	}

	static parseDatabase(data) {
		this.validateTypeof(data, Comment.TYPE);
		return new Comment(data.id, Author.parseDatabase(data.author), data.comment, data.contentType, data.published);
	}
}
