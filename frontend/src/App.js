import { useState, useEffect } from "react";
import "./App.css";
import Login from "./components/Login";
import Router from "./Router";

function App() {

  const [isLogin, setIsLogin] = useState(false);

  useEffect(() => {
    const loggedIn = localStorage.getItem("access_token") ? true : false;
    if (loggedIn) {
      setIsLogin(true);
    }
  }, []);

  const handleLogin = () => {
    setIsLogin(true);
  };

  return (
    isLogin ?
    <Router/> :
    <Login handleLogin={handleLogin}/>
  );
}

export default App;
