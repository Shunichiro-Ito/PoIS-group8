import { Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import Login from '../Login';
import PassForget from '../PassForget';
import CreateNewAccount from '../CreateNewAccount';
import UserProfile from '../UserProfile';
import Home from '../Home';
import UpdatePersonalInfo from '../UpdatePersonalInfo';
import SetTagPage from '../SetTagPage';
import PopularTagsPage from '../SearchPage';

const routes = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Login />} />
      <Route path="/passchange" element={<PassForget />} />
      <Route path="/createnewaccount" element={<CreateNewAccount />} />
      <Route path="/profile" element={<UserProfile />} />
      <Route path="/home" element={<Home />} />
      <Route path="/updatepersonal" element={<UpdatePersonalInfo />} />
      <Route path="/settag" element={<SetTagPage />} />
      <Route path="/search" element={<PopularTagsPage />} />
    </Route>
  )
);
 
export default routes;