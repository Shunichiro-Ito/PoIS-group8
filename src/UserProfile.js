import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Container, Typography, Box, Card, CardContent, Chip, Grid, Button, useRadioGroup, CardHeader, CardActions, Avatar } from '@mui/material';
import Cookies from 'js-cookie';
import Header from "./components/Header";
import ReactionButton from "./components/ReactionButton";
import GppGoodOutlinedIcon from '@mui/icons-material/GppGoodOutlined';
import PostModal from './components/PostModal';

const UserProfile = () => {
  const [user, setUser] = useState(null); // 初期値をnullに設定
  const [posts, setPosts] = useState([]);
  const [content, setContent] = useState("");
  const [tags, setTags] = useState([]);
  const [age, setAge] = useState("");
  const access_token = Cookies.get('access_token');
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPost, setSelectedPost] = useState(null);
  const [indexlist, setIndexlist] = useState({});
  const [taglist, setTaglist] = useState([]);
  const [TAGS, setTAGS] = useState([]);
  const [INDEX,setINDEX] = useState([]);

  const handlePostClick = (post) => {
    setSelectedPost(post);
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
  };

  useEffect(() => {
    let userName;
    const fetchUserData = async () => {
      const page = 1;
      const size = 50;
      try {
        const response2 = await axios.get('http://127.0.0.1:8000/users/me', {
          headers: {
            'Authorization': `bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        setUser(response2.data); // APIレスポンスをuserステートに設定
        console.log(response2.data);
        userName=response2.data.username

        const response3 = await axios.get('http://127.0.0.1:8000/users/interest_tags', {
          headers: {
            'Authorization': `bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        setTAGS(response3.data.available_tags.map((tag) => tag.tag_name));
        setINDEX(response3.data.available_tags.map((tag) => tag.tag_id));
        console.log(TAGS)
        console.log(INDEX)

        const url = `http://127.0.0.1:8000/posts/${userName}?page=${page}&size=${size}`;
        const response = await axios.get(url, {
          headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });

        // レスポンスの処理
        console.log(response.data.items);
        setPosts(response.data.items)
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    
    fetchUserData();
  }, []); // 空の依存配列を渡すことで、コンポーネントがマウントされた時にのみuseEffectが実行される



 return (
   <Container maxWidth="md">
      <Header/>
     <Box my={4}>
       <Typography variant="h4" gutterBottom>
         マイページ
       </Typography>
       {user ? (
         <Card>
           <CardContent>
            <Typography variant="h5" component="div">
                ユーザー名: {user.displayed_name} 
                {user.certified && <GppGoodOutlinedIcon />}
            </Typography>
            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
                marginTop:1,
                marginBottom: 0, // 適宜調整
              }}
            >
            <Box sx={{ marginRight: 2 }} >
            <Button variant="contained" color="primary" component={Link} to="/settag">
            興味のあるタグの選択
            </Button>
            </Box>
            <Box sx={{ marginRight: 2 }} >
            <Button variant="contained" color="primary" component={Link} to="/updatepersonal">
            ユーザー情報変更
            </Button>
            </Box>
            <Button variant="contained" color="primary" component={Link} to="/passchange">
            パスワード変更
            </Button>
            </Box>
          </CardContent>
         </Card>
       ) : (
         <Typography variant="body1">ユーザー情報を読み込み中...</Typography>
       )}
     </Box>

     <Box my={4}>
       <Typography variant="h5" gutterBottom>
         投稿
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
                 subheader={`${post.age || ''}歳`}
                 onClick={() => handlePostClick(post)}
              />
              <CardContent onClick={() => handlePostClick(post)}>
                <Typography variant="h6" component="div">
                  {post.title}
                </Typography>
                <Box mt={1} mb={2}>
                  {post.tag_id.map((tag,index) => (
                    <Chip
                      key={index}
                      label={TAGS && INDEX ? TAGS[INDEX.indexOf(tag)] : `#${tag}`}
                      sx={{ marginRight: 1, marginBottom: 1 }}
                      />
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
          <Typography variant="body1">投稿がありません</Typography>
        )}
      </Container>
     </Box>

   </Container>
 );
};

export default UserProfile;