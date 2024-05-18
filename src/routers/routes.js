import { Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import Login from '../Login';
import PassForget from '../PassForget';
import CreateNewAccount from '../CreateNewAccount';
import UserProfile from '../UserProfile';
import Home from '../Home';

const routes = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Login />} />
      <Route path="/passforget" element={<PassForget />} />
      <Route path="/createnewaccount" element={<CreateNewAccount />} />
      <Route path="/profile" element={<UserProfile />} />
      <Route path="/home" element={<Home />} />
    </Route>
  )
);
 
export default routes;