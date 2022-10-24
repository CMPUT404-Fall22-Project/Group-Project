import React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import { makeStyles } from "@mui/styles";
import Container from "@mui/material/Container";
import { useState } from "react";
import axios from 'axios';

function MadeWithLove() {
	return (
		<Typography variant="body2" color="textSecondary" align="center">
			{"Built with love by the "}
			<Link color="inherit" href="https://material-ui.com/">
				Material-UI
			</Link>
			{" team."}
		</Typography>
	);
}

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

export default function SignUp() {
	const classes = useStyles();

	const [displayName, username] = useState("");
	const [githubURL, url] = useState("");
	const [password, pass] = useState("");

	const handleSignUp = (e) => {
		e.preventDefault();
		const newAuthor = { displayName, githubURL, password };

		console.log(newAuthor);

		// TODO: change endpoint for post
		axios.post('/authors', newAuthor)
		  .then(function (response) {
			console.log(response);
		  })
		  .catch(function (error) {
			console.log(error);
		  });
	};

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
								autoComplete="displayName"
								name="displayName"
								variant="outlined"
								required
								fullWidth
								id="displayName"
								label="Display Name"
								onChange={(e) => username(e.target.value)}
								autoFocus
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
								onChange={(e) => url(e.target.value)}
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
								onChange={(e) => pass(e.target.value)}
							/>
						</Grid>
					</Grid>
					<Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit}>
						Sign Up
					</Button>
					<Grid container justify="flex-end">
						<Grid item>
							<Link href="/signin" variant="body2">
								Already have an account? Sign in
							</Link>
						</Grid>
					</Grid>
				</form>
			</div>
			<Box mt={5}>
				<MadeWithLove />
			</Box>
		</Container>
	);
}
