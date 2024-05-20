
import Sidebar from "./components/Sidebar"; 
import Header from "./components/Header"; 
import PopularTags from "./components/PopularTags";
import ReactionButton from "./components/ReactionButton";
import axios from 'axios';
import { useEffect, useState } from "react";
import "./reset.css";
import { Button, Card, CardContent, TextField, Box, Chip,Container,Paper, Typography } from "@mui/material"; 
import Cookies from 'js-cookie';


import "./App.css";

let TAGS=[];
let INDEX=[];
const POPULAR_TAGS = ["試験", "就活", "生活"];

export const Home = () => {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState([]);
  const [age, setAge] = useState("");
  const access_token = Cookies.get('access_token');

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/interest_tags', {
          headers: {
            'Authorization': `bearer ${access_token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data.available_tags.map((tag) => tag.tag_name))
        TAGS = response.data.available_tags.map((tag) => tag.tag_name);
        INDEX = response.data.available_tags.map((tag) => tag.tag_id);

      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };
    fetchTags();
    fetch("http://localhost:3300/posts")
      .then((res) => res.json())
      .then((json) => setPosts(json));
  }, []);

  const removeTag = (indexToRemove) => {
    setTags((prevTags) => prevTags.filter((_, index) => index !== indexToRemove));
  };

  return (
  <div>
    <Container maxWidth="md">
    <Header />
    <Box>
    <PopularTags  />  
      
{/* ここから投稿コンテナ */}
    <Box sx={{  }}>
      <Container sx={{width:"50%"}}> 
      <TextField 
            fullWidth
            multiline
            rows={1}
            variant="outlined"
            placeholder="タイトルを入力してください"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
      <TextField 
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            placeholder="内容を入力してください"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
      <TextField 
      type="number"
      label="当時の年齢を入力してください"
      value={age}
      onChange={(e) => setAge(e.target.value)}
      style={{ marginRight: "10px" ,width:"100%"}}
      variant="outlined"
      />
        
      <select className="tag-select"
        onChange={(e) => {
          if (e.target.value !== "") {
            setTags((prev) => [...prev, e.target.value]);
          }
        }}
      >
        <option value="">タグを入力してください</option>
        {TAGS.map((tag, index) => {
          return (
            <option key={index} value={tag}>
              {tag}
            </option>
          );
        })}
      </select>
      <Button variant="contained"
      sx={{ backgroundColor: '#89cfeb' , color: '#4d5156' }}
        onClick={async() => {
          const post_tag_id=tags.map(tag => INDEX[TAGS.indexOf(tag)])
          console.log(post_tag_id)
          const url='http://127.0.0.1:8000/posts/submit_post';
          const response = await axios.post(url, 
            {
              "title": title,
              "content": content,
              "age": age,
              "tag_id": post_tag_id,
              "anonymous": true
            }, 
            {headers:{
              'Authorization':`bearer ${access_token}`,
              'Content-Type':'application/json'
            }});
            console.log(response.data)
        }}
        style={{
          outline: "black solid 1px",
          float: "right",
        }}
      >
        投稿を追加
      </Button>
   
      <div>
        {tags.map((tag, index) => (
          <span key={index}>
            #{tag} <span onClick={() => removeTag(index)} style={{cursor: 'pointer', color: 'red'}}>×</span>
          </span>
        ))}
      </div>
      
      </Container> 
{/* ここまで投稿コンテナ */}
{/* ここから投稿表示エリア */}
      <Container sx={{width:"50%"}}>
 
           {posts.map((post) => (
            <Card className="card" key={post.id} sx={{ marginBottom: 2 , overflow: 'auto' }}>
              <div class="card-header">
              <Typography variant="h7">{post.author}</Typography>
              <Typography variant="h7">{post.Age+"歳"}</Typography>
              </div>
              <Box mt={1}>
                  {post.tags.map((tag, idx) => (
                    <Chip key={idx} label={`#${tag}`} style={{ marginRight: 4 ,marginBottom:4}} />

                  ))}
              </Box>
              <CardContent sx={{ marginTop:"5px",border: '1px solid #000',width:"100%",height:"60%" ,overflow: 'auto'}}>
                <Typography variant="body2" >{post.content}</Typography>
              </CardContent>
              <div className="card-footer" >
                <ReactionButton />
              </div>
            </Card>
          ))}
      </Container>
{/* ここまで投稿表示エリア */}
    </Box>
    </Box>
    </Container>
  </div>
  
  );
};

export default Home;