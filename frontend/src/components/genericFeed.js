import { Button, Typography } from "@mui/material";
import React, { Component } from "react";
import Post from "../data/containers/post";
import PaginatedProvider, { GenericElementProvider } from "../data/paginatedProvider";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";
import HourglassEmptyOutlinedIcon from "@mui/icons-material/HourglassEmptyOutlined";
import { NewPostButton } from "./posts/newPost";
import { EditablePostContainer } from "./posts/post";
import { FollowRequestButton } from "./follows/sendFollowRequest";
import { LikesMenuItem } from "./viewLike";
import { LikeButton } from "./likeButton";
import Loader from "./loader";

export class GenericURLFeedComponenet extends Component {
	constructor(props) {
		super(props);
		this.state = {
			posts: [],
			hasAllPosts: false,
			loading: true,
			loadingMorePosts: false,
		};
		this.postSupplier = new PaginatedProvider(new GenericElementProvider(this.props.url));
		this.postSupplier.listen((success, data) => {
			if (success) {
				const formatted = [];
				for (const d of data) {
					try {
						formatted.push(Post.parseDatabase(d));
					} catch (e) {
						console.error(e);
					}
				}
				this.setState((prevState) => {
					return {
						posts: [...prevState.posts, ...formatted],
						hasAllPosts: data.length === 0,
						loading: false,
						loadingMorePosts: false,
					};
				});
			} else {
				NotificationBar.getInstance().addNotification("Failed to load posts.", NotificationBar.NT_ERROR, 10_000);
				this.setState({ loading: false, loadingMorePosts: false });
			}
		});
	}

	supplyMorePosts() {
		this.setState({ loadingMorePosts: true });
		this.postSupplier.requestData();
	}

	componentDidMount() {
		this.supplyMorePosts();
	}

	morePostsButton() {
		var text = "Load more posts...";
		if (this.state.hasAllPosts) {
			text = "All posts loaded!";
		}
		if (this.state.loadingMorePosts) {
			text = "Loading...";
		}
		return (
			<Button
				style={{ marginTop: "0.5em", marginBottom: "0.5em" }}
				disabled={this.state.hasAllPosts || this.state.loadingMorePosts}
				variant="outlined"
				onClick={this.supplyMorePosts.bind(this)}
			>
				{text}
			</Button>
		);
	}

	render() {
		if (this.state.loading) {
			return (
				<div>
					<i>Loading...</i>
					<Loader></Loader>
				</div>
			);
		}
		return (
			<div>
				{this.state.posts.map((x, idx) => (
					<div>
						<EditablePostContainer
							isEditableFunc={() => false}
							data={x}
							key={"Post#" + String(idx)}
						></EditablePostContainer>
						<LikeButton
							authorId={this.props.authorId}
							userId={this.state.userId}
							postId={this.postSupplier.getData()[0][idx].id}
						/>
						<LikesMenuItem
							key="follow-requests"
							variant="outlined"
							onClick={() => this.handleProfileClose()}
							authorId={this.props.authorId}
							userId={this.state.userId}
							postId={this.postSupplier.getData()[0][idx].id}
						></LikesMenuItem>
					</div>
				))}
				{this.morePostsButton()}
			</div>
		);
	}
}

export default class FeedComponent extends GenericURLFeedComponenet {
	constructor(props) {
		super(props);
		const auth = Authentication.getInstance();
		const user = auth.getUser();
		this.state = {
			createdPost: null,
			isCurrentUser: this.props.authorId === user.getId(),
			userId: user.getId(),
			posts: [],
			hasAllPosts: false,
			loading: true,
			loadingMorePosts: false,
		};

		this.postSupplier = new PaginatedProvider(new GenericElementProvider(`${this.props.authorId}/posts/`));
		this.postSupplier.listen((success, data) => {
			if (success) {
				const formatted = data.map((x) => Post.parseDatabase(x));
				this.setState((prevState) => {
					return {
						posts: [...prevState.posts, ...formatted],
						hasAllPosts: data.length === 0,
						loading: false,
						loadingMorePosts: false,
					};
				});
			} else {
				NotificationBar.getInstance().addNotification("Failed to load posts.", NotificationBar.NT_ERROR, 10_000);
				this.setState({ loading: false, loadingMorePosts: false });
			}
		});
	}

	supplyMorePosts() {
		this.postSupplier.requestData();
	}

	componentDidMount() {
		this.supplyMorePosts();
	}

	handleProfileClose() {
		this.setState({ profileMenuAnchor: null });
	}

	render() {
		if (this.state.loading) {
			return (
				<div>
					<i>Loading...</i>
					<Loader></Loader>
				</div>
			);
		}
		if (this.state.isCurrentUser) {
			return (
				<div>
					<NewPostButton></NewPostButton>
					<br></br>
					{this.state.posts.map((x, idx) => (
						<EditablePostContainer data={x} key={"Post#" + String(idx)}></EditablePostContainer>
					))}
					<br></br>
					{this.morePostsButton()}
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
					<FollowRequestButton author={this.props.author} userId={this.state.userId} />
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
				<FollowRequestButton author={this.props.author} userId={this.state.userId} />
				{this.state.posts.map((x, idx) => (
					<div>
						<EditablePostContainer isEditableFunc={() => false} data={x} key={"Post#" + String(idx)} />
						<LikeButton
							authorId={this.props.authorId}
							userId={this.state.userId}
							postId={this.postSupplier.getData()[0][idx].id}
						/>
						<LikesMenuItem
							key="follow-requests"
							variant="outlined"
							onClick={() => this.handleProfileClose()}
							authorId={this.props.authorId}
							userId={this.state.userId}
							postId={this.postSupplier.getData()[0][idx].id}
						></LikesMenuItem>
					</div>
				))}
				{this.morePostsButton()}
			</div>
		);
	}
}
