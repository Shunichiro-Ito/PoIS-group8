import React from 'react';
import { Select, MenuItem, InputLabel, FormControl, Box } from '@mui/material';

const MBTISelect = ({ MBTI, setMBTI, MBTIOptions, label }) => {
  const handleChange = (e) => {
    if (e.target.value !== '') {
      setMBTI(e.target.value);
    }
  };

  return (
    <Box my={3}> {/* my={2}で上下にマージン16pxを設定 */}
    <FormControl fullWidth>
      <InputLabel id="MBTI-select-label">{label}</InputLabel>
      <Select
        labelId="MBTI-select-label"
        value={MBTI}
        onChange={handleChange}
        label="自分の性格"
      >
        <MenuItem value="">
          <em>選択してください</em>
        </MenuItem>
        {MBTIOptions.map((option, index) => (
          <MenuItem key={index} value={option}>
            {option}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
    </Box>
  );
};

export default MBTISelect;