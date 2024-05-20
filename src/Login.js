import * as React from "react";
import { useState } from 'react';
import axios from 'axios';
import "react-router";
import {
  Box,
  Button,
  Container,
  Grid,
  Link,
  TextField,
  Typography,
} from "@mui/material";
import { Link as Llink }  from 'react-router-dom' ;
import Cookies from 'js-cookie';
import Header from "./components/Header"; // Header コンポーネントのインポートを想定しています。

const Login = () => {
  const [name, setName] = useState('');
  const [pass, setPass] = useState('');
  const [error, setError] = useState('');

  const handleNameChange = (event) => {
    setName(event.currentTarget.value);
  };
  const handlePassChange = (event) => {
    setPass(event.currentTarget.value);
  };


  const handleLogin = async(event) => {
    event.preventDefault();
    const data = new URLSearchParams({
      grant_type: '',
      username:name,
      password:pass,
      scope: '',
      client_id: '',
      client_secret: '',
    });
    console.log(name)
    console.log(pass)
    axios
      .post('http://127.0.0.1:8000/users/token', data, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      .then((response) => {
        const access_token = response.data["access_token"]
        Cookies.set('access_token', access_token, { expires: 7 }); // 7日間有効
        Cookies.set('token_type', response.data["token_type"], { expires: 7 }); // 7日間有効
        window.location.href = 'http://localhost:3000/home';
      })
      .catch((error) => {
        console.error(error);
        setError('ログインに失敗しました。メールアドレスとパスワードを確認してください。');
        alert("ユーザーネームかパスワードが違います")
      });
  };


  return (
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
          ログイン
        </Typography>

        <Box component="form" onSubmit={handleLogin} noValidate sx={{ mt:1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            name="name"
            label="ユーザーネーム"
            type="name"
            id="name"
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
            label="パスワード"
            type="password"
            id="password"
            autoComplete="current-password"
            value={pass}
            onChange={handlePassChange}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt:3, mb:2 }}
          >
            ログイン
          </Button>
          

          <Grid container>
            <Grid item xs>
              <Llink to ="/passforget">
                
              </Llink>
            </Grid>

            <Grid item>
              <Llink to ="/createnewaccount">
                新規登録
              </Llink>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default Login;