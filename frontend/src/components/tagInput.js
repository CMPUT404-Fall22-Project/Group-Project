import { Box, Chip, Stack, TextField, Typography } from "@mui/material";
import CancelOutlinedIcon from "@mui/icons-material/CancelOutlined";
import { useRef, useState } from "react";

export default function TagInput({ value, onChange, ...rest }) {
	value = value || [];
	onChange = onChange || function () {};
	const tagRef = useRef();

	//HandleSubmit
	const handleOnSubmit = (e) => {
		e.preventDefault();
		const inputValue = tagRef.current.value;
		if (inputValue && !value.includes(inputValue)) {
			onChange([...value, inputValue]);
			tagRef.current.value = "";
		}
	};

	const handleDelete = (idx) => {
		value.splice(idx, 1);
		onChange(value);
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
							<Stack direction="row" style={{ flexWrap: "wrap", marginRight: value.length ? "0.25em" : "0em" }}>
								{value.map((label, index) => {
									return (
										<Chip
											style={{ height: "100%" }}
											label={label}
											onDelete={handleDelete.bind(this, index)}
											key={index}
										/>
									);
								})}
							</Stack>
						),
					}}
				/>
			</form>
		</Box>
	);
}
