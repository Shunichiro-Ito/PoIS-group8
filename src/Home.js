
import Sidebar from "./components/Sidebar"; 
import Header from "./components/Header"; 
import Cookies from 'js-cookie';


// const mockPosts = [
//   { id: 1, author: "User1", content: "This is the first post" },
//   { id: 2, author: "User2", content: "Here is another post" },
// ];

// const App = () => {
//   const [posts, setPosts] = useState(mockPosts);

//   const handleNewPost = (newContent) => {
//     const newPost = {
//       id: posts.length + 1,
//       author: "UserNew",
//       content: newContent,
//     };
//     setPosts([...posts, newPost]);
//   };

//   return (
//     <Container>
//       <Sidebar />
//       <PostForm onSubmit={handleNewPost} />
//       <Timeline posts={posts} />
//     </Container>
//   );
// };

// export default App;

import { useEffect, useState } from "react";
import "./reset.css";
import { Button, Card, CardContent, TextField, Box, Chip } from "@mui/material"; 
import "./App.css";

const TAGS = ["生活", "勉強", "試験", "就活", "結婚", "受験"];

export const Home = () => {
  const [posts, setPosts] = useState([]);
  const [content, setContent] = useState("");
  const [tags, setTags] = useState([]);
  const [age, setAge] = useState("");
  const access_token = Cookies.get('access_token');

  useEffect(() => {
    fetch("http://localhost:3300/posts")
      .then((res) => res.json())
      .then((json) => setPosts(json));
  }, []);

  const removeTag = (indexToRemove) => {
    setTags((prevTags) => prevTags.filter((_, index) => index !== indexToRemove));
  };

  return (
  <div>
    <Header />
    
    <div className="container"> 
      <div className="input-container">
      {/* <input
        style={{
          height: "200px",
          width: "%",
          outline: "black solid 1px",
        }}
        type="text"
        onChange={(e) => {
          setContent(e.target.value);
        }}
      /> */}
      
      <TextField 
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            placeholder="内容を入力してください"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
      
      </div>
{/*削除機能をつける前のコード */}
      {/* <div>
        {tags.map((tag, index) => (
          <span key={index}>#{tag} </span>
        ))}
      </div> */}

      <div>
        {tags.map((tag, index) => (
          <span key={index}>
            #{tag} <span onClick={() => removeTag(index)} style={{cursor: 'pointer', color: 'red'}}>×</span>
          </span>
        ))}
      </div>
    <div className="select-button-container">
    <input className="age-input"
        type="number"
        placeholder="年齢"
        value={age}
        onChange={(e) => setAge(e.target.value)}
        style={{ marginRight: "10px" }}
      />
     

    
      <select
        onChange={(e) => {
          if (e.target.value !== "") {
            setTags((prev) => [...prev, e.target.value]);
          }
        }}
      >
        <option value="">タグ</option>
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
        onClick={() => {
          fetch("http://localhost:3300/posts", {
            method: "POST",
            body: JSON.stringify({
              content: content,
              author: "author",
              Age:age,
              tags: tags,
            }),
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          });
        }}
        style={{
          outline: "black solid 1px",
          float: "right",
        }}
      >
        投稿を追加
      </Button>
    </div>
      <div>
        {/* {posts.map((post, index) => {
          return (
            <div className="card" key={post.id}>
              {post.id}:{post.content}:{post.author}:
              {post.tags.map((tag, idx) => (
                <span key={idx}>#{tag} </span>
              ))}
            </div>
          );
        })} */}

           {posts.map((post) => (
            <Card className="card" key={post.id} sx={{ marginBottom: 2 }}>
              <CardContent className="post-box">
                <div className="post-author">{post.author}</div>
                <div className="post-age">{post.Age+"歳"}</div>
                <div className="post-content">{post.content}</div>
                
                <Box mt={1}>
                  {post.tags.map((tag, idx) => (
                    <Chip key={idx} label={`#${tag}`} style={{ marginRight: 4 }} />

                  ))}
                </Box>
              </CardContent>
            </Card>
          ))}
      </div>
    </div>
  </div>
  );
};
export default Home;