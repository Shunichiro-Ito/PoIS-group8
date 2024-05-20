import * as React from "react";
import { useState } from 'react';
import axios from 'axios';
import "react-router";
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
} from "@mui/material";
import Cookies from 'js-cookie';
import Header from "./components/Header";

const PassForget = () => {
  const [name, setName] = useState('');
  const [pass, setPass] = useState('');
  const [error, setError] = useState('');

  const handleNameChange = (event) => {
    setName(event.currentTarget.value);
  };
  const handlePassChange = (event) => {
    setPass(event.currentTarget.value);
  };


  const handleChangePass = async(event) => {
    event.preventDefault();
    try {
      const access_token = Cookies.get('access_token');
      console.log(access_token)
      const url='http://127.0.0.1:8000/users/reset_password';
      const response = await axios.post(url, {UserDB: {password: name}, UserReset: {new_password: pass}}, 
      {headers:{
        'Authorization':`bearer ${access_token}`,
        'Content-Type':'application/json'
      }});
      console.log(response.data);
      window.location.href = 'http://localhost:3000/profile';
    } catch (error) {
      console.log(error)
      setError('ログインに失敗しました。メールアドレスとパスワードを確認してください。');
    }
  };


  return (
    <div>
    
    <Container maxWidth="md">
    <Header />
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h4">
          パスワードを変更する
        </Typography>

        <Box component="form" onSubmit={handleChangePass} noValidate sx={{ mt:1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="name"
            label="元のパスワード"
            type="password"
            name="name"
            autoComplete="name"
            autoFocus
            value={name}
            onChange={handleNameChange}
          />

          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="新しいパスワード"
            type="password"
            id="password"
            autoComplete="current-password"
            value={pass}
            onChange={handlePassChange}
          />

          <Button
            margin="normal"
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt:3, mb:2 }}
          >
            進む
          </Button>
        </Box>
      </Box>
    </Container>
    </div>
  );
};

export default PassForget;