import { Box, Stack, TextField, Typography } from "@mui/material";
import CancelOutlinedIcon from "@mui/icons-material/CancelOutlined";
import { useRef, useState } from "react";

// https://blog.theashishmaurya.me/how-to-create-a-tag-input-feature-in-reactjs-and-material-ui

const Tags = ({ data, handleDelete }) => {
	return (
		<Box
			sx={{
				height: "100%",
				display: "flex",
				justifyContent: "center",
				alignContent: "center",
			}}
		>
			<Stack direction="row" gap={1}>
				<Typography>{data}</Typography>
				<CancelOutlinedIcon sx={{ cursor: "pointer" }} onClick={() => handleDelete(data)} />
			</Stack>
		</Box>
	);
};

export default function TagInput({ value, onChange, ...rest }) {
	value = value || [];
	onChange = onChange || function () {};
	const tagRef = useRef();

	//HandleSubmit
	const handleOnSubmit = (e) => {
		e.preventDefault();
		if (tagRef.current.value && !value.includes(tagRef.current.value)) {
			onChange([...value, tagRef.current.value]);
			tagRef.current.value = "";
		}
	};

	const handleDelete = (test) => {
		const newtags = value.filter((val) => val !== test);
		onChange(newtags);
	};

	return (
		<Box sx={{ flexGrow: 1 }}>
			<form onSubmit={handleOnSubmit}>
				<TextField
					inputRef={tagRef}
					variant="standard"
					size="small"
					sx={{ margin: "1rem 0" }}
					margin="none"
					{...rest}
					InputProps={{
						startAdornment: (
							<Box sx={{ margin: "0 0.2rem 0 0", display: "flex" }}>
								{value.map((data, index) => {
									return <Tags data={data} handleDelete={handleDelete} key={index} />;
								})}
							</Box>
						),
					}}
				/>
			</form>
		</Box>
	);
}
