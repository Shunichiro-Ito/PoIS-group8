import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const PostForm = ({ onSubmit }) => {
  const [content, setContent] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(content);
    setContent('');  // 入力フィールドをリセット
  };

  return (
    <Box
        className='post-form'
      component="form"
      onSubmit={handleSubmit}
      sx={{
        mt: 1,
        width: '40%',  // 幅を画面の40%に設定
        margin: 'auto', // 水平方向の中央揃え
        display: 'flex',  // フレックスボックスを使用
        flexDirection: 'column'  // 子要素を縦方向に並べる
      }}
    >
      <TextField
        fullWidth
        id="post-content"
        label="新しい投稿"
        multiline
        rows={4}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        variant="outlined"
        margin="normal"
      />
      <Button type="submit" variant="contained" sx={{ mt: 2 }}>投稿</Button>
    </Box>
  );
};

export default PostForm;