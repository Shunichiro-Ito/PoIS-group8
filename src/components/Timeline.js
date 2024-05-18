// src/components/Timeline.js
import React from 'react';
import Post from './Post';

const Timeline = ({ posts }) => {
  return (
    <div style={{ maxWidth: 600, margin: 'auto' }}>
      {posts.map(post => (
        <Post key={post.id} post={post} />
      ))}
    </div>
  );
};

export default Timeline;