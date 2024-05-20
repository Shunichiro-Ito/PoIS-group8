import * as React from "react";
import { useState, useEffect } from 'react';
import axios from 'axios';
import "react-router";
import {
  Box,
  Chip,
  Container,
  Typography,
  Button,
  Grid,
} from "@mui/material";
import Header from "./components/Header";
import Cookies from 'js-cookie';
import "./reset2.css";
import GenderSelect from './components/GenderSelect';
import MBTISelect from "./components/MBTISelect";

const SetTagPage = () => {
  const [tags, setTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [error, setError] = useState('');
  const access_token = Cookies.get('access_token');
  const handleNextClick = async() => {
    console.log(selectedTags);
    try {
      const url='http://127.0.0.1:8000/users/interest_tags/submit';
      
      const response = await axios.post(url, 
      { interested_tag: selectedTags}, 
      {headers:{
        'Authorization':`bearer ${access_token}`,
        'Content-Type':'application/json'
      }});
      console.log(response.data);
      window.location.href = 'http://localhost:3000/home';
    } catch (error) {
      console.log("No")
      setError('ログインに失敗しました。メールアドレスとパスワードを確認してください。');
    }
  };

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/interest_tags', {
          headers: {
            'Authorization': `bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        setTags(response.data.available_tags);
        console.log(response.data)
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };
    fetchTags();
  }, []);

  const handleTagSelect = (tag) => {
    setSelectedTags((prevSelectedTags) => {
      if (prevSelectedTags.includes(tag.tag_id)) {
        return prevSelectedTags.filter((t) => t !== tag.tag_id);
      } else {
        return [...prevSelectedTags, tag.tag_id];
      }
    });
    console.log(selectedTags);
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
      <Typography variant="h6" gutterBottom>
        興味のあるタグを選択してください
      </Typography>
      
      <Box display="flex" flexWrap="wrap" justifyContent="center" gap={2} marginTop={2}>
        {tags.map((tag) => (
          <Chip
            key={tag.tag_id} // tag_idをkeyとして使用
            label={tag.tag_name} // tag_nameをlabelとして使用
            onClick={() => handleTagSelect(tag)} // 配列全体をhandleTagSelectに渡す
            color={selectedTags.includes(tag.tag_id) ? 'primary' : 'default'}
            sx={{
              fontSize: '1.2rem',
              height: '3rem',
            }}
          />
        ))}
      </Box>
      
    </Box>

    <Grid container>
      <Grid item xs>
      </Grid>
      <Button variant="contained" color="primary" onClick={handleNextClick}>
      設定
      </Button>
    </Grid>
    
    
      
    </Container>
    </div>
  );
};

export default SetTagPage;