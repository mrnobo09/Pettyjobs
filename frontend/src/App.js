import { Routes,Route } from "react-router-dom";
import Login from "./Screens/auth/Login";

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<Login/>}/>
    </Routes>
  );
}

export default App;
