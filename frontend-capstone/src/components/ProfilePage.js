import React, { useState, useEffect } from "react";
import {
  Box,
  Avatar,
  Typography,
  Card,
  CardContent,
  Divider,
  Button,
} from "@mui/material";
import axios from "axios";
import Sidebar from "./Sidebar";

const ProfilePage = () => {
  const [profileData, setProfileData] = useState({
    username: "Loading...",
    email: "Loading...",
    is_student: false,
    is_teacher: false,
    id: null,
  });

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const user = JSON.parse(sessionStorage.getItem("user"));
        if (user && user.username) {
          const response = await axios.get(
            `http://127.0.0.1:8000/users/students/details/${user.username}/`,
            { withCredentials: true }
          );

          setProfileData(response.data);
        } else {
          console.error("No valid user session found.");
        }
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    };

    fetchProfileData();
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        background: "linear-gradient(to bottom, #f4f6f8, #e6f7ff)",
        minHeight: "100vh",
      }}
    >
      {/* Sidebar */}
      <Box
        sx={{
          width: "250px",
          backgroundColor: "#001E3C",
          color: "#fff",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          py: 3,
        }}
      >
        <Sidebar />
      </Box>

      {/* Profile Content */}
      <Box
        sx={{
          flex: 1,
          p: 4,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Card
          sx={{
            width: "100%",
            maxWidth: 600,
            boxShadow: "0 6px 20px rgba(0, 0, 0, 0.2)",
            borderRadius: "12px",
            padding: 4,
            background: "white",
            textAlign: "center",
          }}
        >
          {/* Avatar */}
          <Avatar
            sx={{
              width: 120,
              height: 120,
              margin: "0 auto",
              backgroundColor: "#0288d1",
              color: "#fff",
              fontSize: "2.5rem",
            }}
          >
            {profileData.username[0]?.toUpperCase()}
          </Avatar>

          {/* Username */}
          <Typography
            variant="h5"
            sx={{
              mt: 2,
              fontWeight: "bold",
              color: "#001E3C",
              textShadow: "0px 1px 2px rgba(0, 0, 0, 0.2)",
            }}
          >
            {profileData.username}
          </Typography>
          <Typography
            variant="subtitle1"
            sx={{ color: "#757575", fontStyle: "italic" }}
          >
            ID: {profileData.id || "N/A"}
          </Typography>

          <Divider sx={{ my: 3 }} />

          {/* Contact Section */}
          <CardContent sx={{ textAlign: "left", px: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: "bold", color: "#001E3C" }}>
              Contact
            </Typography>
            <Typography
              variant="body1"
              sx={{
                color: profileData.email ? "#333" : "#b0b0b0",
              }}
            >
              {profileData.email || "No email registered"}
            </Typography>

            <Divider sx={{ my: 2 }} />

            {/* Role Section */}
            <Typography variant="h6" sx={{ fontWeight: "bold", color: "#001E3C" }}>
              Role
            </Typography>
            <Typography
              variant="body1"
              sx={{
                color:
                  profileData.is_student || profileData.is_teacher
                    ? "#333"
                    : "#b0b0b0",
              }}
            >
              {profileData.is_student
                ? "Student"
                : profileData.is_teacher
                ? "Teacher"
                : "No role assigned"}
            </Typography>

            <Divider sx={{ my: 2 }} />

            {/* Biography Section */}
            <Typography variant="h6" sx={{ fontWeight: "bold", color: "#001E3C" }}>
              Biography
            </Typography>
            <Typography
              variant="body1"
              sx={{
                color: "#b0b0b0",
              }}
            >
              No biography has been added
            </Typography>

            <Divider sx={{ my: 2 }} />

            {/* Links Section */}
            <Typography variant="h6" sx={{ fontWeight: "bold", color: "#001E3C" }}>
              Links
            </Typography>
            <Typography
              variant="body1"
              sx={{
                color: "#b0b0b0",
              }}
            >
              No links have been added
            </Typography>
          </CardContent>

          {/* Edit Profile Button */}
        </Card>
      </Box>
    </Box>
  );
};

export default ProfilePage;
