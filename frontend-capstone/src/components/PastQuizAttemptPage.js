import React, { useEffect, useState } from "react";
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Divider,
} from "@mui/material";
import axios from "axios";
import Sidebar from "../components/Sidebar"; // Ensure Sidebar is correctly imported

const PastQuizAttempts = () => {
  const [quizAttempts, setQuizAttempts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuizAttempts = async () => {
      try {
        // Retrieve student session from sessionStorage
        const studentSession = JSON.parse(sessionStorage.getItem("user"));
        if (studentSession && studentSession.id) {
          const studentId = studentSession.id;

          // Fetch quiz attempts for the student
          const response = await axios.get(
            `http://127.0.0.1:8000/knowledge/quizattempt/past_attempts/?student_id=${studentId}`
          );
          setQuizAttempts(response.data);
        } else {
          console.error("Student ID not found in session.");
        }
      } catch (error) {
        console.error("Error fetching quiz attempts:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuizAttempts();
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        background: "linear-gradient(to bottom, #f0f4ff, #e6f7ff)",
        margin: 0,  // Remove any margin between the elements
      }}
    >
      <Sidebar /> {/* Sidebar remains here */}

      <Box
        sx={{
          flex: 1,
          padding: "3rem", // Padding for content
          marginLeft: "250px", // Ensure this value matches the width of the sidebar
        }}
      >
        <Typography
          variant="h4"
          sx={{
            fontWeight: "bold",
            mb: 4,
            color: "#333",
          }}
        >
          Past Quiz Attempts
        </Typography>

        {loading ? (
          <CircularProgress />
        ) : quizAttempts.length === 0 ? (
          <Typography variant="h6" sx={{ color: "#666" }}>
            No quiz attempts found.
          </Typography>
        ) : (
          <Grid container spacing={4} justifyContent="center">
            {quizAttempts.map((attempt) => (
              <Grid item xs={12} sm={6} md={4} key={attempt.id}>
                <Paper
                  elevation={3}
                  sx={{
                    padding: "1.5rem",
                    borderRadius: "10px",
                    backgroundColor: attempt.passed ? "#82e4ab" : "#f68080",
                    boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
                    transition: "transform 0.3s",
                    "&:hover": {
                      transform: "scale(1.03)",
                      boxShadow: "0px 6px 15px rgba(0, 0, 0, 0.2)",
                    },
                  }}
                >
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                      mb: 1,
                      color: "#001E3C",
                    }}
                  >
                    Grade: {attempt.grade}
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{ fontSize: "1rem", color: "#FFF" }}
                  >
                    Unit: {attempt.unit}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography
                    variant="body1"
                    sx={{ fontSize: "1rem", color: "#FFF" }}
                  >
                    Score: {attempt.score}%
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{ fontSize: "1rem", color: "#555" }}
                  >
                    Passed: {attempt.passed ? "Yes" : "No"}
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{
                      fontSize: "0.9rem",
                      color: "#fff",
                      mt: 1,
                    }}
                  >
                    Attempt Date:{" "}
                    {new Date(attempt.attempt_date).toLocaleString()}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Box>
  );
};

export default PastQuizAttempts;
