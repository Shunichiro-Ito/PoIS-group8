// src/components/Post.js
import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const Post = ({ post }) => {
  return (
    <Card sx={{ marginBottom: 2 }}>
      <CardContent>
        <Typography variant="h6" component="div">
          {post.author}
        </Typography>
        <Typography variant="body2">
          {post.content}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default Post;