import NotificationBar from "../../global/centralNotificationBar";
import { tryStringifyObject } from "../../utils/stringify";
import PaginatedProvider, { GenericElementProvider } from "../paginatedProvider";
import Author from "./author";
import DataContainer from "./container";
import Comment from "./comment";
import { isUrlLocal } from "../../utils/local";

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
		this._baseData.commentsSrc = this._baseData.commentsSrc || [];
		if (comments) {
			this._baseData.commentsSrc = comments;
		}

		this._baseData.commentsSrc = this._baseData.commentsSrc.map((x) => Comment.parseDatabase(x));

		this.commentSupplier = new PaginatedProvider(new GenericElementProvider(this._baseData.comments), "comments");
		this.commentSupplier.skip(this._baseData.commentsSrc.length);
		this.commentSupplier.listen((success, data) => {
			if (success) {
				const formatted = data.map((x) => Comment.parseDatabase(x));
				this._baseData.commentsSrc = [...this._baseData.commentsSrc, ...formatted];
			} else {
				NotificationBar.getInstance().addNotification(
					"Failed to load comments." + tryStringifyObject(data),
					NotificationBar.NT_ERROR,
					10_000
				);
			}
		});
	}

	getAuthor() {
		return this._baseData.author;
	}

	getNumComments() {
		return this._baseData.count;
	}

	requestNextComments() {
		return this.commentSupplier.requestData();
	}

	getComments() {
		return this._baseData.commentsSrc;
	}

	getBaseData() {
		return this._baseData;
	}

	isLocalPost() {
		return isUrlLocal(this._baseData.origin);
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
