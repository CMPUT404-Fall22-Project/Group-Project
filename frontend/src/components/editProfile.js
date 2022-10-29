import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom"
import { Box, Grid, Button, TextField } from "@mui/material";


export default function EditProfile() {
    const {id} = useParams()

    const [author, setAuthor] = useState({
        displayName: "",
        gitHub: "",
        pfpURL: "",
    });

    const {displayName, gitHub, pfpURL} = author;

    useEffect(() => {
        axios
            .get('http://127.0.0.1:8000/authors/${id}/')
            .then((res) => {
                console.log(res);
                HandleAuthor(res.data);
            })
            .catch((err) => console.log(err));
        }, []);

    const HandleAuthor = (auth) => {
        // Fill's author with the proper data
        console.log(auth.target.name, ":", auth.target.value);
        setAuthor({ ...author, [auth.target.name]: auth.target.value});
    };

    
    const HandleSubmit = (e) =>{
        axios
            .post('http://127.0.0.1:8000/authors/${id}/')
            .then((res) => console.log(res))
            .catch((err) => console.log(err));
    };


    return (
        <Box sx = {{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
        }}>
            <Box component='form' onSubmit={HandleSubmit} sx={{ mt: 8 }}>
                <Grid container spacing={2}>
                    <Grid item xs={10}>
                        <TextField
                            name='displayName'
                            required
                            fullWidth
                            id="displayName"
                            value={displayName}
                            label="Display Name"
                            onChange={HandleAuthor}
                        />
                    </Grid>
                    <Grid item xs={10}>
                        <TextField
                        name='github'
                        required
                        fullWidth
                        id="github"
                        value={gitHub}
                        label="Github URL"
                        onChange={HandleAuthor}
                        />
                    </Grid>
                    <Grid item xs={10}>
                        <TextField
                        name='pfpURL'
                        required
                        fullWidth
                        id="pfpURL"
                        value={pfpURL}
                        label="Pfp URL"
                        onChange={HandleAuthor}
                        />
                    </Grid>
                    <Grid item xs={5}>
                        <Button
                        type="submit"
                        variant="contained"
                        sx ={{ mb: 10 }}>
                        Submit 
                        </Button>
                    </Grid>
                </Grid>
            </Box>
        </Box>
    )
}