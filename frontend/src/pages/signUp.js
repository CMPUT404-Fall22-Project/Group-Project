import React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import CheckCircleOutlinedIcon from "@mui/icons-material/CheckCircleOutlined";
import Typography from "@mui/material/Typography";
import { makeStyles } from "@mui/styles";
import Container from "@mui/material/Container";
import { useState } from "react";
import axios from "axios";
import NotificationBar from "../global/centralNotificationBar";
import preProcessAxios from "../data/serverResponse";

const useStyles = makeStyles((theme) => ({
	"@global": {
		body: {
			backgroundColor: theme.palette.common.white,
		},
	},
	paper: {
		marginTop: theme.spacing(8),
		display: "flex",
		flexDirection: "column",
		alignItems: "center",
	},
	avatar: {
		margin: theme.spacing(1),
		backgroundColor: theme.palette.secondary.main,
	},
	form: {
		width: "100%", // Fix IE 11 issue.
		marginTop: theme.spacing(3),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
}));

export default function SignUpPage() {
	const classes = useStyles();

	const [username, setUsername] = useState("");
	const [displayName, setDisplayName] = useState("");
	const [githubURL, setUrl] = useState("https://github.com/");
	const [password, setPassword] = useState("");
	const [passwordConfirm, setPasswordConfirm] = useState("");
	const [error, setError] = useState("");
	const [posted, setPosted] = useState("");
	const [success, setSuccess] = useState("");
	const [profileImage, setProfileImage] = useState(
		"https://user-images.githubusercontent.com/71047780/198223700-cf5b87b1-6318-4419-b1cf-4ceee56281eb.png"
	);

	const postUser = () => {
		const data = {
			author_data: {
				displayName: displayName,
				github: githubURL,
				profileImage: profileImage,
			},
			user_data: {
				username: username,
				password: password,
			},
		};
		preProcessAxios(
			axios({
				method: "post",
				url: process.env.REACT_APP_HOST + `users/signup/`,
				data: data,
			})
		)
			.then((resp) => {
				setSuccess(1);
			})
			.catch((error) => {
				setPosted(0);
			});
	};

	const handleSignUp = (e) => {
		e.preventDefault();

		if (
			!username ||
			!displayName ||
			!profileImage ||
			!githubURL ||
			!password ||
			!passwordConfirm ||
			password !== passwordConfirm
		) {
			setError(1);
			return;
		}

		if (posted) {
			return;
		}

		setPosted(1);

		// first, check if the name is taken
		axios({
			method: "get",
			url: process.env.REACT_APP_HOST + `users/check/${username}/`,
		})
			.then((resp) => {
				if (resp.value) {
					NotificationBar.getInstance().addNotification(
						`User with name ${username} already exists.`,
						NotificationBar.NT_ERROR,
						10_000
					);
					setPosted(0);
					return;
				} else {
					postUser();
				}
			})
			.catch((error) => {
				NotificationBar.getInstance().addNotification(
					"Unknown error: " + String(error),
					NotificationBar.NT_ERROR,
					1e10
				);
				setPosted(0);
			});
	};

	const checkError = (data, isPassword) => {
		if (!error) {
			return {};
		}
		if (!data) {
			return { error: true, helperText: "This field cannot be empty" };
		}
		if (isPassword && password !== passwordConfirm) {
			return { error: true, helperText: "Passwords do not match" };
		}
	};

	if (success) {
		return (
			<Container component="main">
				<CssBaseline />
				<div className={classes.paper}>
					<Avatar className={classes.avatar}>
						<CheckCircleOutlinedIcon />
					</Avatar>
					<Typography component="h1" variant="h4" style={{ maxWidth: "100%", margin: "1em" }}>
						Account successfully created!
					</Typography>
					<Typography component="h1" variant="h6" style={{ maxWidth: "50%", textAlign: "center", color: "#919191" }}>
						<i>
							Before you can use your account, you will need to be authorized by an administrator. Please be patient as
							the manual review process may take some time.
						</i>
					</Typography>
				</div>
			</Container>
		);
	}

	return (
		<Container component="main" maxWidth="xs">
			<CssBaseline />
			<div className={classes.paper}>
				<Avatar className={classes.avatar}>
					<LockOutlinedIcon />
				</Avatar>
				<Typography component="h1" variant="h5">
					Sign up
				</Typography>
				<form className={classes.form} noValidate onSubmit={handleSignUp}>
					<Grid container spacing={2}>
						<Grid item xs={12}>
							<TextField
								autoComplete="username"
								name="username"
								variant="outlined"
								required
								fullWidth
								id="username"
								label="Username"
								onChange={(e) => setUsername(e.target.value)}
								defaultValue={username}
								autoFocus
								{...checkError(username, false)}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								autoComplete="displayName"
								name="displayName"
								variant="outlined"
								required
								fullWidth
								id="displayName"
								label="Display Name"
								onChange={(e) => setDisplayName(e.target.value)}
								defaultValue={displayName}
								{...checkError(displayName, false)}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								autoComplete="profileImage"
								name="profileImage"
								variant="outlined"
								required
								fullWidth
								id="profileImage"
								label="Profile image URL"
								onChange={(e) => setProfileImage(e.target.value)}
								defaultValue={profileImage}
								{...checkError(profileImage, false)}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								id="githubURL"
								label="Github URL"
								name="githubURL"
								onChange={(e) => setUrl(e.target.value)}
								defaultValue={githubURL}
								{...checkError(githubURL, false)}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								name="password"
								label="Password"
								type="password"
								id="password"
								autoComplete="current-password"
								onChange={(e) => setPassword(e.target.value)}
								defaultValue={password}
								{...checkError(password, true)}
							/>
						</Grid>
						<Grid item xs={12}>
							<TextField
								variant="outlined"
								required
								fullWidth
								name="passwordConfirm"
								label="Confirm Password"
								type="password"
								id="passwordConfirm"
								autoComplete="current-password"
								onChange={(e) => setPasswordConfirm(e.target.value)}
								defaultValue={passwordConfirm}
								{...checkError(passwordConfirm, true)}
							/>
						</Grid>
					</Grid>
					<Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit}>
						Sign Up
					</Button>
					<Grid container justify="flex-end">
						<Grid item>
							<Link href="/" variant="body2">
								Already have an account? Sign in
							</Link>
						</Grid>
					</Grid>
				</form>
			</div>
		</Container>
	);
}
