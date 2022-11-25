import React, { useEffect, useState } from "react";
import CommentListItem from "./commentListItem";
import axios from "axios";

// https://levelup.gitconnected.com/fetch-api-data-with-axios-and-display-it-in-a-react-app-with-hooks-3f9c8fa89e7b

export default function CommentsListDialog(props) {
	const [comments, getComments] = useState("");
	const [author, getAuthor] = useState("");
	const { baseURL } = props;

	useEffect(() => {
		axiosGetComments();
		axiosGetAuthor();
	}, []);

	const axiosGetComments = () => {
		axios({
			method: "get",
			url: baseURL + "/comments",
		}).then(function (response) {
			const allComments = response.data.items;
			getComments(allComments);
		});
	};

	const axiosGetAuthor = () => {
		// get author url using regex
		// (if prettier breaks this, the expression is ".+?(?=(\/post))")
		// prettier-ignore
		var authorRegex = new RegExp(".+?(?=(\/post))");
		var authorURL = authorRegex.exec(baseURL);
		axios({
			method: "get",
			url: authorURL[0],
		}).then(function (response) {
			var authorData = response.data;
			getAuthor(authorData);
		});
	};

	return <CommentListItem comments={comments} author={author}></CommentListItem>;
}
