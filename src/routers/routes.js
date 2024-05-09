import { Route, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';
import Login from '../Login';
import PassForget from '../PassForget';

const routes = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Login />} />
      <Route path="/passforget" element={<PassForget />} />
    </Route>
  )
);
 
export default routes;