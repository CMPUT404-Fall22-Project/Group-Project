import { Backdrop } from "@mui/material";
import { withStyles } from "@mui/styles";

// https://stackoverflow.com/a/60933935

export default withStyles({
	root: {
		position: "absolute",
		zIndex: 1,
	},
})(Backdrop);
