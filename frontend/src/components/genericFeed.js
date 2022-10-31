import { Paper } from "@mui/material";
import React, { Component } from "react";
import Post from "../data/containers/post";
import PaginatedProvider, { GenericElementProvider } from "../data/paginatedProvider";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";
import NewPost, { NewPostButton } from "./posts/newPost";
import PostViewComponent, { EditablePostContainer } from "./posts/post";

export default class FeedComponent extends Component {
	constructor(props) {
		super(props);
		const auth = Authentication.getInstance();
		const user = auth.getUser();
		this.state = {
			createdPost: null,
			isCurrentUser: this.props.authorId === user.getId(),
			posts: [],
		};

		this.postSupplier = new PaginatedProvider(
			new GenericElementProvider(process.env.REACT_APP_HOST + "authors/" + props.authorId + "/posts/")
		);
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
		if (this.state.isCurrentUser) {
			return (
				<div>
					<NewPostButton></NewPostButton>
					{this.state.posts.map((x, idx) => (
						<EditablePostContainer data={x} key={"Post#" + String(idx)}></EditablePostContainer>
					))}
				</div>
			);
		}
		return (
			<div>
				{this.state.posts.map((x, idx) => (
					<EditablePostContainer
						isEditableFunc={() => false}
						data={x}
						key={"Post#" + String(idx)}
					></EditablePostContainer>
				))}
			</div>
		);
	}
}
