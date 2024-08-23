import { Routes,Route } from "react-router-dom";
import Login from "./Screens/auth/Login";
import {Provider} from 'react-redux'
import Store from "./State/Store.js";

function App() {
  return (
    <Provider store = {Store}>
      <Routes>
        <Route path="/auth" element={<Login/>}/>
      </Routes>
    </Provider>
  );
}

export default App;
