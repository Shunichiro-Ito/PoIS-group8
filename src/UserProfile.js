import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Container, Typography, Box, Card, CardContent, Grid, Button } from '@mui/material';
import Cookies from 'js-cookie';

const UserProfile = () => {
   const [user, setUser] = useState(null);
   const [posts, setPosts] = useState([]);
   const access_token = Cookies.get('access_token');

   useEffect(() => {
   const fetchUserData = async () => {
      try {     
         const response1 = await axios.get('http://127.0.0.1:8000/users/me',
         {headers:{
            'Authorization':`bearer ${access_token}`,
            'Content-Type':'application/json'
         }});
         const response2 = await axios.get('http://127.0.0.1:8000/users/johndoe/posts',
         {headers:{
            'Authorization':`bearer ${access_token}`,
            'Content-Type':'application/json'
         }});

         setUser(response1.data);
         setPosts(response2.data.posts);
      } catch (error) {
         console.error('Error fetching user data:', error);
      }
   };

   fetchUserData();
 }, []);

 return (
   <Container maxWidth="md">
     <Box my={4}>
       <Typography variant="h4" gutterBottom>
         マイページ
       </Typography>
       {user ? (
         <Card>
           <CardContent>
             <Typography variant="h5" component="div">
               ユーザー名: {user.username}
             </Typography>
             <Button variant="contained" color="primary" component={Link} to="/passforget">
            パスワード変更
            </Button>
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
       <Grid container spacing={2}>
         {posts.map((post) => (
           <Grid item xs={12} sm={6} md={4} key={post.id}>
             <Card>
               <CardContent>
                 <Typography gutterBottom variant="h6" component="div">
                   {post.title}
                 </Typography>
                 <Typography variant="body2" color="text.secondary">
                   {post.content}
                 </Typography>
               </CardContent>
             </Card>
           </Grid>
         ))}
       </Grid>
     </Box>

   </Container>
 );
};

export default UserProfile;