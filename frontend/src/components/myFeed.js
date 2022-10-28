import { Paper } from "@mui/material";
import React, { Component } from "react";
import Post from "../data/containers/post";
import PaginatedProvider, { GenericElementProvider } from "../data/paginatedProvider";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";
import NewPost, { NewPostButton } from "./posts/newPost";
import PostViewComponent from "./posts/post";

export default class MyFeed extends Component {
	constructor(props) {
		super(props);
		this.state = {
			createdPost: null,
			posts: [],
		};
		const auth = Authentication.getInstance();
		const user = auth.getUser();
		this.postSupplier = new PaginatedProvider(new GenericElementProvider(user.getUrl() + "/posts/"));
		this.postSupplier.listen((success, data) => {
			if (success) {
				const formatted = data.map((x) => Post.parseDatabase(x));
				this.setState((prevState) => {
					return {
						posts: [...prevState.posts, ...formatted],
					};
				});
			} else {
				NotificationBar.getInstance().addNotification("Failed to load posts.", NotificationBar.NT_ERROR, 10_000);
			}
		});
	}

	supplyMorePosts() {
		this.postSupplier.requestData();
	}

	componentDidMount() {
		this.supplyMorePosts();
	}

	render() {
		return (
			<div>
				<NewPostButton></NewPostButton>
				{this.state.posts.map((x, idx) => (
					<PostViewComponent data={x} key={"Post#" + String(idx)}></PostViewComponent>
				))}
			</div>
		);
	}
}
