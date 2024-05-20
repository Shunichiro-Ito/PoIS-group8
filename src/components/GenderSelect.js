import React from 'react';
import { Select, MenuItem, InputLabel, FormControl, Box } from '@mui/material';

const GenderSelect = ({ gender, setgender, genderOptions, label }) => {
  const handleChange = (e) => {
    if (e.target.value !== '') {
      setgender(e.target.value);
    }
  };

  return (
   <Box my={2}> {/* my={2}で上下にマージン16pxを設定 */}
    <FormControl fullWidth>
      <InputLabel id="gender-select-label">{label}</InputLabel>
      <Select
        labelId="gender-select-label"
        value={gender}
        onChange={handleChange}
        label="自分の性別"
        required
        fullWidth
        name="mbti"
        type="mbti"
        id="mbti"
        autoComplete="current-mbti"
      >
        <MenuItem value="">
          <em>選択してください</em>
        </MenuItem>
        {genderOptions.map((option, index) => (
          <MenuItem key={index} value={option}>
            {option}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
    </Box>
  );
};

export default GenderSelect;