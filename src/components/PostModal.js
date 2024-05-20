import React from 'react';
import {
   Modal,
   Card,
   CardHeader,
   Avatar,
   Typography,
   CardContent,
   Box,
   Chip,
   CardActions,
   IconButton,
 } from '@mui/material';
import ReactionButton from "./ReactionButton";

const PostModal = ({ open, handleClose, post }) => {
  // postがnullの場合は何も描画しない
  if (!post) {
    return null;
  }

  return (
    <Modal open={open} onClose={handleClose}>
      <Box sx={style}>
      <Card sx={{ maxWidth: 345, marginBottom: 2 }}>
      <CardHeader
         avatar={
            <Avatar>
               {post.author ? post.author.charAt(0).toUpperCase() : ''}
            </Avatar>
         }
         title={post.author || ''}
         subheader={`${post.age || ''}歳`}
      />
      <CardContent>
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
      </Box>
    </Modal>
  );
};

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

export default PostModal;