import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import axios from "axios";

import { createTheme, ThemeProvider } from "@mui/material/styles";

axios.defaults.withCredentials = true;

const theme = createTheme({
	palette: {
		primary: {
			light: "#95d5b2",
			main: "#007C41",
			dark: "#007C41",
			contrastText: "#fff",
		},
		secondary: {
			light: "#95d5b2",
			main: "#007C41",
			dark: "#007C41",
			contrastText: "#000",
		},
	},
	typography: {
		fontFamily: ["Open Sans", "sans-serif"].join(","),
		fontSize: 14,
		fontWeightLight: 300,
		fontWeightRegular: 400,
		fontWeightMedium: 500,
	},
	overrides: {
		MuiFormControlLabel: {
			label: {
				fontSize: 14,
			},
		},
	},
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
	<ThemeProvider theme={theme}>
		<App />
	</ThemeProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
