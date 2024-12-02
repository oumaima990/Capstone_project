import React, { useState, useEffect } from "react";
import profilePic from "../images/student_icon.png"
import {
  Box,
  Avatar,
  Typography,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
} from "@mui/material";
import {
  School,
  BarChart,
  History,
  Person,
} from "@mui/icons-material";
import { useNavigate, useLocation } from "react-router-dom";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [userData, setUserData] = useState({
    username: "Loading...",
    email: "Loading...",
    profilePicture: profilePic,
  });

  useEffect(() => {
    const fetchUserData = () => {
      try {
        const user = JSON.parse(sessionStorage.getItem("user"));
        if (user && user.username) {
          setUserData({
            username: user.username,
            email: user.email || "email@example.com",
            profilePicture:profilePic ,
          });
        } else {
          console.error("No valid user session found.");
          navigate("/login");
        }
      } catch (error) {
        console.error("Error retrieving user session:", error);
      }
    };

    fetchUserData();
  }, [navigate]);

  const isActive = (path) => location.pathname === path;

  return (
    <Box
      sx={{
        width: "280px",
        background: "linear-gradient(to bottom, #6f84ea, #6f84ea)",
        color: "#000",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        position: "fixed",
        borderRight: "1px solid #E0E0E0",
        boxShadow: "2px 0px 8px rgba(0, 0, 0, 0.1)",
        paddingTop: "1rem",
        overflowY: "auto",
      }}
    >
      {/* Logo Section */}
      <Box sx={{ p: 2, textAlign: "center" }}>
        <Typography
          variant="h5"
          sx={{
            color: "#ffffff",
            fontWeight: "bold",
            fontSize: "1.5rem",
            background: "-webkit-linear-gradient(45deg, #ffffff, #ffffff)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Interactive Arabic Learning
        </Typography>
      </Box>

      <Divider sx={{ mb: 2 }} />

      {/* Profile Section */}
      <Box sx={{ p: 2, textAlign: "center" }}>
        <Avatar
          src={userData.profilePicture}
          alt="Profile"
          sx={{
            width: 90,
            height: 90,
            margin: "0 auto",
            border: "3px solid #ffffff",
            boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.2)",
          }}
        />
        <Typography
          variant="body1"
          sx={{
            mt: 1,
            fontWeight: "bold",
            color: "#ffffff",
            fontSize: "1rem",
          }}
        >
          {userData.username}
        </Typography>
        <Typography
          variant="body2"
          sx={{
            color: "#000",
            fontSize: "0.85rem",
          }}
        >
          {userData.email}
        </Typography>
      </Box>

      <Divider sx={{ mb: 2 }} />

      {/* Navigation */}
      <List>
        {[
          { text: "Profile", icon: <Person />, path: "/profile" },
          { text: "Check Progress", icon: <BarChart />, path: "/keep-track" },
          { text: "Learning Page", icon: <School />, path: "/units" },
          { text: "Past Quiz Attempts", icon: <History />, path: "/quiz-attempts" },
        ].map((item) => (
          <Tooltip key={item.text} title={item.text} placement="right" arrow>
            <ListItemButton
              onClick={() => navigate(item.path)}
              sx={{
                backgroundColor: isActive(item.path) ? "#EBF0F5" : "transparent",
                color: isActive(item.path) ? "#000" : "#ffffff",
                borderRadius: "8px",
                margin: "0.5rem",
                "&:hover": {
                  backgroundColor: "#000",
                  color: "#fff",
                  boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
                },
                transition: "all 0.3s ease",
              }}
            >
              <ListItemIcon>
                {React.cloneElement(item.icon, {
                  sx: { color: isActive(item.path) ? "#000" : "#FFF" },
                })}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                sx={{ fontWeight: isActive(item.path) ? "bold" : "normal" }}
              />
            </ListItemButton>
          </Tooltip>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;
