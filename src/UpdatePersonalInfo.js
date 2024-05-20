import * as React from "react";
import { useState ,useEffect} from 'react';
import axios from 'axios';
import "react-router";
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Select,
} from "@mui/material";
import Header from "./components/Header";
import Cookies from 'js-cookie';
import "./reset2.css";
import GenderSelect from './components/GenderSelect';
import MBTISelect from "./components/MBTISelect";

const MBTI = ["INTJ（建築家）","INTP（論理学者）","ENTJ（指揮官）","ENTP（討論者）","INFJ（提唱者）",
"INFP（仲介者）","ENFJ（主人公）","ENFP（運動家）","ISTJ（管理者）","ISFJ（擁護者）","ESTJ（幹部）",
"ESFJ（領事）","ISTP（巨匠）","ISFP（冒険家）","ESFP（エンターテイナー）","ESTP（起業家）"];
const GENDER = ["男性", "女性"]

const UpdatePersonalInfo = () => {
  const [name, setName] = useState('');
  const [displayed_name, setDisplayedName] = useState('');
  const [pass, setPass] = useState('');
  const [occupation, setOccupation] = useState('')
  const [error, setError] = useState('');
  const [mbti, setMBTI] = useState([]);
  const [gender, setgender] = useState([]);
  const [birthdate, setBirthdate] = useState('');
  const [user, setUser] = useState(null);
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
  


  const handleCreateNewAccount = async(event) => {
    event.preventDefault();
    console.log(gender)
    console.log(occupation)
    console.log(birthdate)
    console.log(mbti)
    try {
      const url='http://127.0.0.1:8000/users/update_personal_info/submit';
      const response = await axios.post(url, 
      {
        "birth": birthdate,
        "gender": gender,
        "occupation": occupation,
        "mbti": mbti.slice(0,4),
      }, 
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

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/me', {
          headers: {
            'Authorization': `bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data);
        setUser(response.data); // APIレスポンスをuserステートに設定
        setgender(response.data.gender);
        setBirthdate(response.data.birth);
        setOccupation(response.data.occupation);
        //setMBTI(response.data.mbti);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };
    fetchUserData();
  }, []); // 空の依存配列を渡すことで、コンポーネントがマウントされた時にのみuseEffectが実行される


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
          アカウント情報の変更
        </Typography>

        <Box component="form" onSubmit={handleCreateNewAccount} noValidate sx={{ mt:1 }}>
          
          <TextField
            margin="normal"
            required
            fullWidth
            name="occupation"
            label="1．自分の職業"
            type="occupation"
            id="occupation"
            autoComplete="current-occupation"
            value={occupation}
            onChange={handleOccupation}
          />

          <div>
            <MBTISelect
              MBTI={mbti}
              setMBTI={setMBTI}
              MBTIOptions={MBTI}
              label="2．自分の性格"
            />
          </div>

          {/*
          <div>
            <label htmlFor="birthdate" >　4．自分の生年月日　</label>
            <input
              type="date"
              id="birthdate"
              value={birthdate}
              onChange={(e) => setBirthdate(e.target.value)}
              required
            />
          </div>
          */}

          

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

export default UpdatePersonalInfo;