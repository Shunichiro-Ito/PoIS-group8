import React, { useState } from "react";
import { Box, IconButton, Typography } from "@mui/material";
import SentimentSatisfiedAltIcon from "@mui/icons-material/SentimentSatisfiedAlt";
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import SentimentVeryDissatisfiedIcon from "@mui/icons-material/SentimentVeryDissatisfied";

const ReactionButton = ({ Icon, count, setCount, selected, setSelected }) => {
  const toggleReaction = () => {
    setSelected(!selected);
    setCount(selected ? count - 1 : count + 1);
  };

  return (
    <Box display="flex" alignItems="center" mx={1}>
      <IconButton onClick={toggleReaction} color={selected ? "primary" : "default"}>
        {Icon}
      </IconButton>
      <Typography component="span">{count}</Typography>
    </Box>
  );
};

const Reactions = ({good, impossible, early}) => {
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(good);

  const [agreed, setAgreed] = useState(false);
  const [agreesCount, setAgreesCount] = useState(impossible);

  const [understood, setUnderstood] = useState(false);
  const [understandsCount, setUnderstandsCount] = useState(early);

  return (
    <Box display="flex" justifyContent="flex-end" mt={2}>
      <ReactionButton
        Icon={<SentimentSatisfiedAltIcon />}
        count={likesCount}
        setCount={setLikesCount}
        selected={liked}
        setSelected={setLiked}
      />
      <ReactionButton
        Icon={<SentimentVeryDissatisfiedIcon />}
        count={null}
        setCount={setAgreesCount}
        selected={agreed}
        setSelected={setAgreed}
      />
      <ReactionButton
        Icon={<ArrowCircleUpIcon />}
        count={understandsCount}
        setCount={setUnderstandsCount}
        selected={understood}
        setSelected={setUnderstood}
      />
    </Box>
  );
};

export default Reactions;