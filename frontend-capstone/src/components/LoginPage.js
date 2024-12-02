import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css"; // Custom CSS for additional styles
import loginImage from "../images/image_login.png";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/users/students/login/",
        { username, password },
        { withCredentials: true } // Include credentials for session-based authentication
      );

      const { success, user_type, student_name, redirect_url, id } = response.data;

      if (success) {
        // Save session-based user data in sessionStorage
        sessionStorage.setItem(
          "user",
          JSON.stringify({
            username,
            user_type,
            id, // Include the id as part of the user object
          })
        );

        // Redirect the user and pass session data to the redirected page
        navigate(redirect_url, { state: { username, user_type, id } });
      } else {
        setError("Invalid username or password.");
      }
    } catch (err) {
      setError("Login failed. Please try again.");
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-image">
          <img src={loginImage} alt="Login Illustration" />
        </div>
        <div className="login-form">
          <h1>Welcome to The Reactive Inteface for Arabic Learning!</h1>
          <p>Please sign in to your account and start the adventure</p>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                className="form-control"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && <p className="error">{error}</p>}
            <div className="form-options">
              <div>
              </div>
            </div>
            <button type="submit" className="btn btn-primary btn-block">
              Login
            </button>
          </form>
          <div className="form-footer">
            <p>
              New on our platform? <a href="/signup">Create an account</a>
            </p>
            <div className="social-login">
              <button className="social-btn facebook">F</button>
              <button className="social-btn twitter">T</button>
              <button className="social-btn github">G</button>
              <button className="social-btn google">G</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
