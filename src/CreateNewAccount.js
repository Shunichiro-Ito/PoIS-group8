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
import Header from "./components/Header";
import Cookies from 'js-cookie';
import "./reset2.css";
import "./App.css";

const MBTI = ["INTJ（建築家）","INTP（論理学者）","ENTJ（指揮官）","ENTP（討論者）","INFJ（提唱者）",
"INFP（仲介者）","ENFJ（主人公）","ENFP（運動家）","ISTJ（管理者）","ISFJ（擁護者）","ESTJ（幹部）",
"ESFJ（領事）","ISTP（巨匠）","ISFP（冒険家）","ESFP（エンターテイナー）","ESTP（起業家）"];
const SEX = ["男性", "女性","その他"]

const CreateNewAccount = () => {
  const [name, setName] = useState('');
  const [displayed_name, setDisplayedName] = useState('');
  const [pass, setPass] = useState('');
  const [occupation, setOccupation] = useState('')
  const [error, setError] = useState('');
  const [mbti, setMBTI] = useState([]);
  const [sex, setSex] = useState([]);
  const access_token = Cookies.get('access_token');

  const handleNameChange = (event) => {
    setName(event.currentTarget.value);
  };
  const handleDisplayedNameChange = (event) => {
    setDisplayedName(event.currentTarget.value);
  };
  const handlePassChange = (event) => {
    setPass(event.currentTarget.value);
  };
  const handleOccupation = (event) => {
    setOccupation(event.currentTarget.value);
  };
  const [birthdate, setBirthdate] = useState('');


  const handleCreateNewAccount = async(event) => {
    event.preventDefault();
    console.log(name)
    console.log(pass)
    console.log(mbti)
    console.log(birthdate)
    console.log(occupation)
    console.log(mbti.slice(0,4))
    
    try {
      const url='http://127.0.0.1:8000/users/register';
      const response = await axios.post(url, 
      {
        "password": pass,
        "birth": birthdate,
        "gender": "f",
        "occupation": occupation,
        "mbti": mbti.slice(0,4),
        "username": name,
        "displayed_name": name}, 
      {headers:{
        'Authorization':`bearer ${access_token}`,
        'Content-Type':'application/json'
      }});
      
      // アクセストークンを保存する (CookieやlocalStorage、Redux storeなど)
      // ...

      // 認証が必要なページへリダイレクトする
      console.log("Yes")
      console.log(response.data);
    } catch (error) {
      console.log("No")
      setError('ログインに失敗しました。メールアドレスとパスワードを確認してください。');
    }
  };


  return (
    <div>
      <Header />
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h4">
          アカウントの作成
        </Typography>

        <Box component="form" onSubmit={handleCreateNewAccount} noValidate sx={{ mt:1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="name"
            label="ユーザーネーム"
            name="name"
            autoComplete="name"
            autoFocus
            value={name}
            onChange={handleNameChange}
          />

        {/*  <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="表示するユーザーネーム"
            type="displayed_name"
            id="displayed_name"
            autoComplete="displayed_name"
            value={displayed_name}
            onChange={handleDisplayedNameChange}
          /> */}

          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="設定するパスワード"
            type="password"
            id="password"
            autoComplete="current-password"
            value={pass}
            onChange={handlePassChange}
          />

          <TextField
            margin="normal"
            required
            fullWidth
            name="occupation"
            label="自分の職業"
            type="occupation"
            id="occupation"
            autoComplete="current-occupation"
            value={occupation}
            onChange={handleOccupation}
          />

          <select
            onChange={(e) => {
              if (e.target.value !== "") {
                setSex(e.target.value);
              }
            }}
          >
            <option value="">自分の性別</option>
            {SEX.map((sex, index) => {
              return (
                <option key={index} value={sex}>
                  {sex}
                </option>
              );
            })}
          </select>
        

          <div>
            <label htmlFor="birthdate" >自分の生年月日　</label>
            <input
              type="date"
              id="birthdate"
              value={birthdate}
              onChange={(e) => setBirthdate(e.target.value)}
              required
            />
          </div>
          
        

          <select
            onChange={(e) => {
              if (e.target.value !== "") {
                setMBTI(e.target.value);
              }
            }}
          >
            <option value="">自分の性格</option>
            {MBTI.map((mbti, index) => {
              return (
                <option key={index} value={mbti}>
                  {mbti}
                </option>
              );
            })}
          </select>

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

export default CreateNewAccount;