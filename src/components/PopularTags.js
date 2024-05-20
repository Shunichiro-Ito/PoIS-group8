// src/components/PopularTags.js

import React from "react";
import { Box, Chip, Typography, Grid} from "@mui/material";

const POPULAR_TAGS = ["試験", "就活", "生活"];

const PopularTags = () => {
  return (

    <Box className="sidebar" flex={1} mr={2} 
    sx={{
            border: '1px solid #ccc',
            borderRadius: '8px',
            padding: '16px',
            backgroundColor: '#f9f9f9',
            maxWidth: '25%',
            marginRight: '16px' , 
            marginTop: '100px', 
    
        }}>
      
      <Typography variant="h6">人気のタグ</Typography>
      {POPULAR_TAGS.map((tag, index) => (
        <Chip key={index} label={`#${tag}`} sx={{ marginBottom: 1 ,marginTop:1}} />
      ))}
    </Box>
   
  );
};

export default PopularTags;