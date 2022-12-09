import React, { useEffect, useState } from "react";
import CommentListItem from "./commentListItem";
import axios from "axios";

// https://levelup.gitconnected.com/fetch-api-data-with-axios-and-display-it-in-a-react-app-with-hooks-3f9c8fa89e7b

export default function CommentsListDialog(props) {
	const [comments, getComments] = useState("");
	const { baseURL } = props;
	/* 	const [author, getAuthor] = useState("");
	var uniqueAuthorObjects = {}; */

	useEffect(() => {
		axiosGetComments();
	}, []);

	const axiosGetComments = () => {
		axios({
			method: "get",
			url: baseURL + "/comments",
		}).then(function (response) {
			const allComments = response.data.items;
			getComments(allComments);
			/* 			// https://stackoverflow.com/a/35092559
			// https://stackoverflow.com/a/58429784
			const uniqueAuthors = [...new Set(allComments.map((item) => item.author.id))]; // [ 'A', 'B']
			// ok this is hacky i cannot check for all unique authors directly from the comments
			for (var i = 0; i < allComments.length; i++) {
				uniqueAuthorObjects[allComments[i].author.id] = allComments[i].author;
			}
			getAuthor(uniqueAuthorObjects); */
		});
	};

	/* 	const axiosGetAuthor = () => {
		// not used anymore
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
	}; */

	return <CommentListItem comments={comments}></CommentListItem>;
}
