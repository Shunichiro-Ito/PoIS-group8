import * as React from 'react';
import { AppBar, Box, Toolbar, IconButton, Typography, MenuItem, Menu} from '@mui/material';
import { Menu as MenuIcon, AccountCircle} from '@mui/icons-material';
import SearchIcon from '@mui/icons-material/Search';
import { useState } from 'react';
import Cookies from 'js-cookie';

export default function PrimarySearchAppBar() {
  // メニューの開閉を管理するためのstate
  const [anchorEl, setAnchorEl] = useState(null);

  // anchorElがnullでない場合にtrueを返す(メニューが開いているかどうか)
  const isMenuOpen = Boolean(anchorEl);

  // プロフィールメニューを開く
  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  // メニューを閉じる
  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfileClick = () => {
    window.location.href = 'http://localhost:3000/profile';
  };

  const handleHome = () => {
    window.location.href = 'http://localhost:3000/home';
  };

  const handleLogoutClick = () => {
    Cookies.remove('access_token');
    Cookies.remove('token_type');
    Cookies.remove();
    window.location.href = 'http://localhost:3000/'
  }

  
  const menuId = 'primary-search-account-menu';
  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      id={menuId}
      keepMounted
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      open={isMenuOpen}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={handleProfileClick}>Profile</MenuItem>
      <MenuItem onClick={handleLogoutClick}>Logout</MenuItem>
    </Menu>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ bgcolor: '#1976d2' }}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            sx={{ mr: 2 }} // margin-right: 2
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1 }}
            onClick={handleHome}
          >
            Fails Tales
          </Typography>
          <Box sx={{ display: 'flex' }}>
            
            <IconButton
              size="large"
              color="inherit"
              onClick={() => window.location.href = 'http://localhost:3000/search'}>

             
            <SearchIcon />
            </IconButton>

            <IconButton
              size="large"
              edge="end"
              aria-controls={menuId}
              aria-haspopup="true"
              onClick={handleProfileMenuOpen}
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>
      {renderMenu}
    </Box>
  );
}