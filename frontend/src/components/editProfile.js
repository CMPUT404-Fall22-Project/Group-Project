import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Grid, Button, TextField } from "@mui/material";
import Authentication from "../global/authentication";
import NotificationBar from "../global/centralNotificationBar";


export default function EditProfile() {
    const {id} = Authentication.getInstance().getUser().getId();

    const [author, setAuthor] = useState({
        displayName: "",
        gitHub: "",
        pfpURL: "",
    });

    const {displayName, gitHub, pfpURL} = author;

    useEffect(() => {
        axios
            .get(process.env.REACT_APP_HOST + 'authors/${id}/')
            .then((res) => {
                console.log(res);
                HandleAuthor(res.data);
            })
            .catch((err) => console.log(err));
        }, []);

    const HandleAuthor = (auth) => {
        // Fill's author's fields with the proper data
        console.log(auth.target.name, ":", auth.target.value);
        setAuthor({ ...author, [auth.target.name]: auth.target.value});
    };

    
    const HandleSubmit = (e) =>{
        axios
            .post(process.env.REACT_APP_HOST + 'authors/${id}/')
            .then((res) => NotificationBar.getInstance().addNotification("Edited successfully!", NotificationBar.NT_SUCCESS))
            .catch((err) => NotificationBar.getInstance().addNotification(err, NotificationBar.NT_ERROR))
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
                        sx ={{ mb: 10 }}
                        onClick={() => {
                            HandleSubmit();
                        }}>
                        Submit 
                        </Button>
                    </Grid>
                </Grid>
            </Box>
        </Box>
    )
}