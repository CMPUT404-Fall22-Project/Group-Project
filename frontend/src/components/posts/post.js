import React, { Component } from "react";

export default class PostViewComponent extends Component {
	constructor(props) {
		super(props);
		if (!data) {
			throw new Error("Missing required prop 'data'");
		}
		this.state = {
			container: props.data || null,
		};
	}

	render() {
		return <Pape elevation={3} variant="outlined" />;
	}
}
