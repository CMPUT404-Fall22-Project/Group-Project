import { Paper, Typography } from "@mui/material";
import React, { Component } from "react";
import Post from "../data/containers/post";
import PaginatedProvider, { GenericElementProvider } from "../data/paginatedProvider";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";
import HourglassEmptyOutlinedIcon from "@mui/icons-material/HourglassEmptyOutlined";
import { NewPostButton } from "./posts/newPost";
import { EditablePostContainer } from "./posts/post";

export default class FeedComponent extends Component {
	constructor(props) {
		super(props);
		const auth = Authentication.getInstance();
		const user = auth.getUser();
		this.state = {
			createdPost: null,
			isCurrentUser: this.props.authorId === user.getId(),
			posts: [],
			hasAllPosts: false,
		};

		var postsUrl = props.authorId + "/posts/";
		if (!this.state.isCurrentUser) {
			postsUrl = process.env.REACT_APP_HOST + `authors/${postsUrl}`;
		}
		this.postSupplier = new PaginatedProvider(new GenericElementProvider(postsUrl));
		this.postSupplier.listen((success, data) => {
			if (success) {
				const formatted = data.map((x) => Post.parseDatabase(x));
				this.setState((prevState) => {
					return {
						posts: [...prevState.posts, ...formatted],
						hasAllPosts: data.length === 0,
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
		if (this.state.posts.length === 0 && this.state.hasAllPosts) {
			const styles = {
				opacity: 0.5,
				padding: "1em",
			};
			return (
				<div>
					<Typography variant="h4" style={styles}>
						<i>Nothing to see here...</i>
					</Typography>
					<HourglassEmptyOutlinedIcon style={{ fontSize: "10em", opacity: 0.5 }}></HourglassEmptyOutlinedIcon>
					<Typography variant="h4" style={styles}>
						Check back later to see new posts from this author!
					</Typography>
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
