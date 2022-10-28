import React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import { makeStyles } from "@mui/styles";
import { useState } from "react";
import background from "../static/back.webp";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";

const useStyles = makeStyles((theme) => ({
	root: {
		height: "100vh",
	},
	image: {
		backgroundImage: `url(${background})`,
		backgroundRepeat: "no-repeat",
		backgroundSize: "cover",
		backgroundPosition: "center",
	},
	paper: {
		margin: theme.spacing(8, 4),
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
		marginTop: theme.spacing(1),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
}));

const SignInPage = () => {
	const classes = useStyles();
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");

	const handleLogin = (e) => {
		e.preventDefault();

		if (!username || !password) {
			setError(1);
			return;
		}

		Authentication.getInstance()
			.authenticate(username, password)
			.catch((request) => {
				NotificationBar.getInstance().addNotification(request.response.data, NotificationBar.NT_ERROR, 15_000);
			});
	};

	const checkError = (data) => {
		if (!error) {
			return {};
		}
		if (!data) {
			return { error: true, helperText: "This field cannot be empty" };
		}
	};

	var text = "Sign in";
	if (window.location.pathname !== "/") {
		text = (
			<span>
				Sign in to continue to
				<br /> <i style={{ color: "#afafaf" }}>{window.location.pathname}</i>
			</span>
		);
	}

	return (
		<Grid container component="main" className={classes.root}>
			<CssBaseline />
			<Grid item xs={false} sm={4} md={7} className={classes.image} />
			<Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
				<div className={classes.paper}>
					<Avatar className={classes.avatar}>
						<LockOutlinedIcon />
					</Avatar>
					<Typography component="h1" variant="h5" align="center" style={{ maxWidth: "100%" }}>
						{text}
					</Typography>
					<form className={classes.form} noValidate onSubmit={handleLogin}>
						<TextField
							variant="outlined"
							margin="normal"
							required
							fullWidth
							id="username"
							label="Username"
							name="username"
							autoComplete="username"
							onChange={(e) => setUsername(e.target.value)}
							{...checkError(username)}
							autoFocus
						/>
						<TextField
							variant="outlined"
							margin="normal"
							required
							fullWidth
							name="password"
							label="Password"
							type="password"
							id="password"
							autoComplete="current-password"
							{...checkError(password)}
							onChange={(e) => setPassword(e.target.value)}
						/>
						<Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit}>
							Sign In
						</Button>
						<Grid container>
							<Grid item xs></Grid>
							<Grid item>
								<Link href="/signup" variant="body2">
									{"Don't have an account? Sign Up"}
								</Link>
							</Grid>
						</Grid>
					</form>
				</div>
			</Grid>
		</Grid>
	);
};

export default SignInPage;
