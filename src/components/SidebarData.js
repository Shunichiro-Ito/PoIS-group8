import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';



// SidebarDataの定義と型注釈
export const SidebarData = [
    {
        title: "APP",
    },
    {
        title: "Home",
        icon: <HomeIcon />,
        link: "/home",
    },
    {
        title: "Search",
        icon: <SearchIcon />,
        link: "/search", // リンク先を "/search" に変更しています
    },
];