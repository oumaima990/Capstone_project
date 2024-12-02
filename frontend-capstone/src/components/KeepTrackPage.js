import React, { useEffect, useState } from "react";
import { Box, Typography, Card, Grid, LinearProgress, Divider } from "@mui/material";
import Sidebar from "../components/Sidebar"; // Ensure this path is correct
import { Doughnut } from "react-chartjs-2";
import axios from "axios";
import { Stepper, Step, StepLabel } from "@mui/material"; // Add this import

// Import necessary Chart.js components
import {
  Chart as ChartJS,
  ArcElement,   // Ensure ArcElement is imported
  Tooltip,
  Legend,
  Title,
  CategoryScale,
  LinearScale
} from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  Title,
  CategoryScale,
  LinearScale
);

const CheckProgressPage = () => {
  const [knowledgeComponents, setKnowledgeComponents] = useState([]);
  const [unitProgress, setUnitProgress] = useState([]);
  const [quizAttempts, setQuizAttempts] = useState([]); // Store quiz attempts
  const [doughnutData, setDoughnutData] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProgressData = async () => {
      try {
        // Retrieve student ID from sessionStorage
        const studentSession = JSON.parse(sessionStorage.getItem("user"));

        if (studentSession && studentSession.id) {
          const studentId = studentSession.id;

          // Fetch knowledge components, unit progress, and quiz attempts
          const progressResponse = await axios.get(
            `http://127.0.0.1:8000/users/students/get_student_knowledge_components/?student_id=${studentId}`
          );
          const unitResponse = await axios.get(
            `http://127.0.0.1:8000/knowledge/unit/student_progress/?student_id=${studentId}`
          );
          const quizResponse = await axios.get(
            `http://127.0.0.1:8000/knowledge/quizattempt/get_student_progress_info/?student_id=${studentId}`
          );

          // Set data for knowledge components and unit progress
          const progressData = progressResponse.data.knowledge_components;
          setKnowledgeComponents(progressData);

          const unitData = unitResponse.data;
          setUnitProgress(unitData);

          const quizData = quizResponse.data;
          setQuizAttempts(quizData);

          // Prepare doughnut chart data for mastery percentages
          const labels = progressData.map((kc) => kc.component_name);
          const percentages = progressData.map((kc) => kc.mastery_percentage);
          setDoughnutData({
            labels: labels,
            datasets: [
              {
                data: percentages,
                backgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56",
                  "#4CAF50",
                  "#F44336",
                ],
                hoverBackgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56",
                  "#4CAF50",
                  "#F44336",
                ],
              },
            ],
          });
        } else {
          setError("Student ID not found in session.");
        }
      } catch (error) {
        console.error("Error fetching progress data:", error);
        setError("Failed to fetch progress data.");
      }
    };

    fetchProgressData();
  }, []);

  // Filter only the passed quizzes
  const passedQuizzes = quizAttempts.filter((attempt) => attempt.passed);

  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        background: "linear-gradient(to bottom, #f0f4ff, #e6f7ff)",
      }}
    >
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <Box sx={{ flex: 1, ml: "300px", p: 3 }}>
        <Typography
          variant="h4"
          sx={{
            textAlign: "center",
            fontWeight: "bold",
            color: "#001E3C", // Dark text color
            mb: 4,
          }}
        >
          Progress Dashboard
        </Typography>

        {error ? (
          <Typography
            variant="h6"
            sx={{
              textAlign: "center",
              color: "red",
              mt: 4,
            }}
          >
            {error}
          </Typography>
        ) : (
          <Grid container spacing={3}>
            {/* Unit Progress (Stepper) - Top Section */}
            <Grid item xs={12}>
              <Card
                sx={{
                  p: 3,
                  textAlign: "center",
                  borderRadius: "12px",
                  background: "#FFFFFF",
                  boxShadow: "0 4px 15px rgba(0, 0, 0, 0.1)",
                }}
              >
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Unit Progress
                </Typography>
                <Stepper alternativeLabel activeStep={unitProgress.findIndex(unit => unit.unlocked)}>
                  {unitProgress.map((unit, index) => (
                    <Step key={unit.unit}>
                      <StepLabel
                        sx={{
                          color: unit.unlocked ? "#6f84ea" : "#6f84ea",
                          fontWeight: unit.unlocked ? "bold" : "normal",
                        }}
                      >
                        {`Grade ${unit.grade}, Unit ${unit.unit} - ${
                          unit.unlocked ? "Unlocked" : "Locked"
                        }`}
                      </StepLabel>
                    </Step>
                  ))}
                </Stepper>
              </Card>
            </Grid>
            {/* Progress Summary with Linear Progress Bars */}
            <Grid item xs={12} md={6}>
              <Card
                sx={{
                  p: 3,
                  borderRadius: "12px",
                  background: "#FFFFFF",
                  boxShadow: "0 4px 15px rgba(0, 0, 0, 0.1)",
                }}
              >
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Progress Summary
                </Typography>
                <Box>
                  {knowledgeComponents.map((kc) => (
                    <Box key={kc.component_name} sx={{ mb: 2 }}>
                      <Typography
                        variant="body1"
                        sx={{ fontWeight: "bold", color: "#001E3C" }}
                      >
                        {kc.component_name}:{" "}
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={kc.mastery_percentage}
                        sx={{
                          height: 10,
                          borderRadius: 5,
                          backgroundColor: "#e0e0e0",
                          "& .MuiLinearProgress-bar": {
                            backgroundColor: "#82e4ab",
                          },
                        }}
                      />
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        {kc.mastery_percentage}% Mastery
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </Card>
            </Grid>

            {/* Passed Quizzes Display */}
            <Grid item xs={12}>
              <Card
                sx={{
                  p: 3,
                  textAlign: "center",
                  borderRadius: "12px",
                  background: "#FFFFFF",
                  boxShadow: "0 4px 15px rgba(0, 0, 0, 0.1)",
                }}
              >
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Passed Quizzes
                </Typography>
                {passedQuizzes.length > 0 ? (
                  passedQuizzes.map((quiz, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Typography variant="body1" sx={{ fontWeight: "bold" }}>
                        {`Unit ${quiz.unit}, Grade ${quiz.grade}`}
                      </Typography>
                      <Typography variant="body2">Score: {quiz.score}%</Typography>
                      <Divider sx={{ my: 1 }} />
                    </Box>
                  ))
                ) : (
                  <Typography>No passed quizzes found.</Typography>
                )}
              </Card>
            </Grid>
          </Grid>
        )}
      </Box>
    </Box>
  );
};

export default CheckProgressPage;
