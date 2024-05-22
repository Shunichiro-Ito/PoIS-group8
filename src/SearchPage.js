import React, { useState, useEffect } from 'react';
import { Container, Box, Grid, Typography, Paper, TextField, Button ,  Card, CardContent, Chip, useRadioGroup, CardHeader, CardActions, Avatar} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import Header from './components/Header'
import axios from 'axios';
import Cookies from 'js-cookie';
import PostModal from './components/PostModal';
import ReactionButton from "./components/ReactionButton";
import GppGoodOutlinedIcon from '@mui/icons-material/GppGoodOutlined';

const SearchPage = () => {
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [posts, setPosts] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPost, setSelectedPost] = useState(null);
  let search_result;
  const access_token = Cookies.get('access_token');
  let feedback_token;

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handlePostClick = async(post) => {
    setSelectedPost(post);
    setModalOpen(true);
    const feedback = Cookies.get('session_id');
    const url = `http://127.0.0.1:8000/posts/post_id/${post.post_id}?session=${feedback}`;

    try {
      const response = await axios.post(
        url,
        {},
        {
          headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json',
            'accept': 'application/json'
          }
        }
      );

      // レスポンスの処理
      console.log(response.data);
      console.log("Yes")
    } catch (error) {
      console.log("No")
      setError('ログインに失敗しました。メールアドレスとパスワードを確認してください。');
    }
  };

  const handleModalClose = () => {
    setModalOpen(false);
  };


  const handleSearchSubmit = async(event) => {
    event.preventDefault();
    const url = 'http://127.0.0.1:8000/search';
    const params = {
      cat: 'all',
      string: searchTerm,
      encoding: 'utf-8',
      errors: 'replace'
    };
    try {
      const response = await axios.post(url, {}, {
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Content-Type': 'application/json'
        },
        params: params
      });
      // レスポンスの処理
      console.log(response.data);
      console.log("Yes")
      search_result=response.data;
      setPosts(search_result["Display Posts"]);
      feedback_token=search_result["session_id"]
      const thirtyMinutesFromNow = new Date(Date.now() + 30 * 60 * 1000);
      Cookies.set('session_id', feedback_token, { expires: thirtyMinutesFromNow }); 
      console.log(search_result["Display Posts"])
    } catch (error) {
      console.log("No")
      setError('ログインに失敗しました。メールアドレスとパスワードを確認してください。');
    }
  };
  useEffect(() => {
    
  }, [search_result]); // 空の依存配列を渡すことで、コンポーネントがマウントされた時にのみuseEffectが実行される



  return (
   <>
    <Container maxWidth="md">
    <Header />
      <Box sx={{ textAlign: 'center', margin: '20px 0' }}>
        <TextField 
          variant="outlined" 
          placeholder="キーワードを入力..." 
          fullWidth 
          sx={{ marginTop: 2 }}
          value={searchTerm}
          type="search"
          onChange={handleSearchChange}
        />
        {/* 提出ボタン */}
        <Button 
          variant="contained" 
          color="primary" 
          sx={{ marginTop: 2 }} 
          startIcon={<SearchIcon />} 
          onClick={handleSearchSubmit}
        >
          検索
        </Button>
      </Box>
      <Box my={4}>
       <Typography variant="h5" gutterBottom>
         検索結果
       </Typography>
       <Container sx={{width:"50%"}}>
        {posts && posts.length > 0 ? (
          <>
            {posts.map((post) => (
              <Card sx={{ maxWidth: 345, marginBottom: 2 }} >
              <CardHeader
                avatar={
                  <Avatar>
                    {post.author ? post.author.charAt(0).toUpperCase() : ''}
                  </Avatar>
                }
                title={post.author || ''}
                subheader={
                  <Box display="flex" alignItems="center">
                    <span>{`${post.age || ''} 歳`}</span>
                    {post.certified && (
                      <Box ml={1} display="flex">
                        <GppGoodOutlinedIcon />
                      </Box>
                    )}
                  </Box>
                }
                onClick={() => handlePostClick(post)}
                align="left"
              />
              <CardContent onClick={() => handlePostClick(post)}>
                <Typography variant="h6" component="div">
                  {post.title}
                </Typography>
                <Box mt={1} mb={2}>
                  {post.tag_id.map((tag, idx) => (
                    <Chip key={idx} label={`#${tag}`} sx={{ marginRight: 1, marginBottom: 1 }} />
                  ))}
                </Box>
                <Typography variant="body1" sx={{ maxHeight: 150, overflow: 'auto' }}>
                  {post.content}
                </Typography>
              </CardContent>
              <CardActions disableSpacing>
                <ReactionButton good={post.good} impossible={post.impossible} early={post.early} />
                <Box ml="auto">
                  <Typography variant="body2" sx={{ marginLeft: 1 }}>
                    {post.post_date}
                  </Typography>
                </Box>
              </CardActions>
            </Card>
            ))}
            <PostModal open={modalOpen} handleClose={handleModalClose} post={selectedPost} />
          </>
        ) : (
          <Typography variant="body1">検索結果がありません</Typography>
        )}
      </Container>
     </Box>
    </Container>
    </>
  );
};

export default SearchPage;