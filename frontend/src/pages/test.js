import React, { Component } from "react";
import { Button } from "@mui/material";
import { withStyles } from "@mui/styles";
import "./test.css";
import { APPLICATION_NAME } from "../constants";
import background from "../static/back.webp";
import { useState } from "react";
import cn from "classnames";
import ThumbUpIcon from '@mui/icons-material/ThumbUp';

export const LikeButton = () => {
    const [liked, setLiked] = useState(null);
    const [clicked, setClicked] = useState(false);
  
    return (
      <button
        onClick={() => {
            setLiked(!liked);
            setClicked(true);
        }}
        onAnimationEnd={() => setClicked(false)}
        className={cn("like-button-wrapper", {
          liked,
          clicked,
        })}
      >
        <div className="like-button">
            <ThumbUpIcon />
            <span>Like</span>
            <span className={cn("suffix", { liked })}>d</span>
        </div>
      </button>
    );
  };

const LoginButton = withStyles((theme) => ({
	root: {
		color: "#575757",
		backgroundColor: "#ffffff",
		fontWeight: "100",
		fontSize: "0.75rem",
		width: "15em",
		height: "3em",
		"&:hover": {
			backgroundColor: "#eeeeee",
		},
	},
}))(Button);

class LoginComponent extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {}

	login() {}

	render() {
		return (
			<div
				className="Fade-In"
				style={{
					backgroundImage: `url(${background})`,
					backgroundRepeat: "no-repeat",
					backgroundSize: "cover",
					top: "0",
					height: "100%",
					width: "100%",
					position: "absolute",
					overflow: "clip",
				}}
			>
				<div style={{ height: "50%", minHeight: "1250px", position: "relative" }}>
					<div className="outer-login-box">
						<div className="login-box">
							<div className="login-page-container">
								<div className="login-instructions">{APPLICATION_NAME}</div>

								<div style={{ padding: "1em" }}></div>
								<LoginButton variant="contained" onClick={this.login.bind(this, !this.props.check)}>
									Login
								</LoginButton>
							</div>
                            <LikeButton className="like-button-wrapper">
                                Like
                            </LikeButton>
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default LoginComponent;

