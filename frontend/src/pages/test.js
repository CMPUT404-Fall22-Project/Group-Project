import React, { Component } from "react";
import { Button } from "@mui/material";
import { withStyles } from "@mui/styles";
import "./test.css";
import { APPLICATION_NAME } from "../constants";
import background from "../static/back.webp";
import { useState } from "react";
import cn from "classnames";
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import List from "@mui/material/List";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import DeleteIcon from "@mui/icons-material/Delete";
import Stack from '@mui/material/Stack';
import { styled } from "@mui/material/styles";
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';


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

function generate(element: React.ReactElement) {
    return [0, 1, 2, 3,4,5,6,7,8,9,10,11,12].map((value) =>
      React.cloneElement(element, {
        key: value
      })
    );
  }
  
  const Demo = styled("div")(({ theme }) => ({
    backgroundColor: theme.palette.background.paper
  }));

  export function TopAppBar() {
    return (
      <div style={{ width: "50%", height: "100%", position: "absolute" }}>
        <Box sx={{ flexGrow: 1,maxWidth: 1000 }}>
          <AppBar position="static">
            <Toolbar>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="menu"
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Follow Requests
              </Typography>
            </Toolbar>
          </AppBar>
          <div style={{ width: "100%", height: "100%", position: "absolute", overflow: "auto" }}>
            <InteractiveList>
            </InteractiveList>
          </div>
        </Box>
      </div>
    );
  }

  export function InteractiveList() {
    const [dense] = React.useState(false);
    const username = "username"
    const name = "Firstname Lastname";
  
    return (
      <Box sx={{ flexGrow: 1}}>
        <Grid container spacing={0}>
        </Grid>
        <Grid container spacing={5}>
          <Grid item xs={12} md={0}>
            <Demo>
              <List dense={dense}>
                {generate(
                  <ListItem
                    secondaryAction={
                      <Stack spacing={0.5} direction="row">
                        <Button variant="outlined">Accept</Button>
                        <Button variant="outlined">Reject</Button>
                      </Stack>
                    }
                  >
                    
                    <ListItemAvatar>
                      <Avatar>
                        <DeleteIcon />
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={username}
                      secondary={name}
                    />
                  </ListItem>
                )}
              </List>
            </Demo>
          </Grid>
        </Grid>
      </Box>
    );
  }
  

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
        <LikeButton className="like-button-wrapper">
          Like
          </LikeButton>
					<div className="outer-login-box">
              <div classname="follower-requests">
                <TopAppBar classname="top-app-bar">
                </TopAppBar>
              </div>
            </div>
					</div>
				</div>
		);
	}
}

export default LoginComponent;

