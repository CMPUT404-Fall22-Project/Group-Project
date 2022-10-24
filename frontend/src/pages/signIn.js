import React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import { makeStyles } from "@mui/styles";
import { useState } from "react";

const MadeWithLove = () => (
	<Typography variant="body2" color="textSecondary" align="center">
		{"Built with love by the "}
		<Link color="inherit" href="https://material-ui.com/">
			Material-UI
		</Link>
		{" team."}
	</Typography>
);

const useStyles = makeStyles((theme) => ({
	root: {
		height: "100vh",
	},
	image: {
		backgroundImage: "url(https://source.unsplash.com/random)",
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

const SignInSide = () => {
	const classes = useStyles();
	const [displayName, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const handleLogin = (e) => {
		e.preventDefault();
		const userLogin = { displayName, password };

		fetch("http://localhost:3000", {
			// TODO: fix hardcoding url
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(userLogin),
		});
	};

	return (
		<Grid container component="main" className={classes.root}>
			<CssBaseline />
			<Grid item xs={false} sm={4} md={7} className={classes.image} />
			<Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
				<div className={classes.paper}>
					<Avatar className={classes.avatar}>
						<LockOutlinedIcon />
					</Avatar>
					<Typography component="h1" variant="h5">
						Sign in
					</Typography>
					<form className={classes.form} noValidate onSubmit={handleLogin}>
						<TextField
							variant="outlined"
							margin="normal"
							required
							fullWidth
							id="displayName"
							label="Display Name"
							name="displayName"
							autoComplete="displayName"
							onChange={(e) => setUsername(e.target.value)}
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
							onChange={(e) => setPassword(e.target.value)}
						/>
						<FormControlLabel control={<Checkbox value="remember" color="primary" />} label="Remember me" />
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
						<Box mt={5}>
							<MadeWithLove />
						</Box>
					</form>
				</div>
			</Grid>
		</Grid>
	);
};

export default SignInSide;
