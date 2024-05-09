import { Box, CircularProgress } from "@mui/material";
import React from "react";

const Loading = ({ height = "" }) => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height={height}
    >
      <CircularProgress />
    </Box>
  );
};

export default Loading;