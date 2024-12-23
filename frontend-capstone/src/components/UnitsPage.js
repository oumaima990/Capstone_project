import React, { useState, useEffect } from "react";
import {
  Box,
  Grid,
  Paper,
  Typography,
  AppBar,
  Toolbar,
  Button,
  CircularProgress,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import axios from "axios";

const UnitsPage = () => {
  const [units, setUnits] = useState([]);
  const [texts, setTexts] = useState([]);
  const [selectedUnitTitle, setSelectedUnitTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUnits = async () => {
      try {
        const studentSession = JSON.parse(sessionStorage.getItem("user"));

        if (studentSession && studentSession.id) {
          const studentId = studentSession.id;

          const response = await axios.get(
            `http://127.0.0.1:8000/knowledge/unit/student_progress/?student_id=${studentId}`
          );

          setUnits(response.data);
        } else {
          console.error("Student ID not found in session.");
          navigate("/login");
        }
      } catch (error) {
        console.error("Error fetching units:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUnits();
  }, [navigate]);

  const fetchTexts = async (unit, grade) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/knowledge/text/get-texts/?grade=${grade}&unit=${unit}`
      );
      setTexts(response.data);
      setSelectedUnitTitle(`Grade ${grade}, Unit ${unit}`);
    } catch (err) {
      console.error("Error fetching texts:", err);
    }
  };

  const handleTextClick = (textId) => {
    navigate(`/text/${textId}`);
  };

  const handleQuizClick = (unit, grade) => {
    navigate(`/quiz?unit=${unit}&grade=${grade}`);
  };

  const handleUnitClick = (unit) => {
    if (unit.unlocked) {
      fetchTexts(unit.unit, unit.grade);
    } else {
      alert("This unit is locked. Complete the required quiz to unlock.");
    }
  };

  const renderUnitsByGrade = () => {
    const grades = [...new Set(units.map((unit) => unit.grade_name))];

    return grades.map((gradeName, index) => (
      <Box key={index} sx={{ mb: 5 }}>
        <Typography
          variant="h5"
          sx={{
            fontWeight: "bold",
            color: "#001E3C",
            mb: 3,
            textAlign: "center",
          }}
        >
          {gradeName}
        </Typography>
        <Grid container spacing={4} justifyContent="center">
          {units
            .filter((unit) => unit.grade_name === gradeName)
            .map((unit, idx) => (
              <Grid item xs={12} sm={6} md={4} key={idx}>
                <Paper
                  elevation={4}
                  sx={{
                    p: 3,
                    textAlign: "center",
                    borderRadius: "10px",
                    background: unit.unlocked
                      ? "linear-gradient(to bottom, #ffffff, #f0f4ff)"
                      : "linear-gradient(to bottom, #99a9f8, #8398fe)",
                    border: "1px solid #FFF",
                    cursor: unit.unlocked ? "pointer" : "not-allowed",
                    transition:
                      "transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out",
                    "&:hover": {
                      transform: unit.unlocked ? "scale(1.05)" : "none",
                      boxShadow: unit.unlocked
                        ? "0 8px 20px rgba(0, 0, 0, 0.2)"
                        : "none",
                    },
                  }}
                  onClick={() => handleUnitClick(unit)}
                >
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                      color: unit.unlocked ? "#001E3C" : "#fff",
                    }}
                  >
                    {unit.unit_name}
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      mt: 1,
                      fontWeight: "bold",
                      color: unit.unlocked ? "#82e4ab" : "#f68080",
                    }}
                  >
                    {unit.unlocked ? "Unlocked" : "Locked"}
                  </Typography>
                </Paper>
              </Grid>
            ))}
        </Grid>
      </Box>
    ));
  };

  const renderTexts = () => (
    <Box sx={{ mt: 5, px: { xs: 2, sm: 5 } }}>
      <Typography
        variant="h5"
        sx={{
          mb: 4,
          fontWeight: "bold",
          color: "#001E3C",
          textAlign: "center",
        }}
      >
        Texts in {selectedUnitTitle}
      </Typography>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2, // Spacing between text items
          alignItems: "center", // Center the list
        }}
      >
        {texts.map((text) => (
          <Paper
            key={text.id}
            elevation={3}
            sx={{
              width: "100%",
              maxWidth: "600px", // Optional: Limit the width for better readability
              p: 2,
              textAlign: "center",
              borderRadius: "10px",
              cursor: "pointer",
              transition:
                "transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out",
              "&:hover": {
                transform: "scale(1.03)",
                boxShadow: "0 6px 15px rgba(0, 0, 0, 0.2)",
              },
            }}
            onClick={() => handleTextClick(text.id)}
          >
            <Typography
              variant="h6"
              sx={{
                fontWeight: "bold",
                color: "#001E3C",
              }}
            >
              {text.title}
            </Typography>
          </Paper>
        ))}
      </Box>
      {/* Render the quiz button only once */}
      {texts.length > 0 && (
        <Box
          sx={{
            mt: 5,
            textAlign: "center",
            p: 2,
            borderRadius: "10px",
            backgroundColor: "#000",
            color: "#fff",
            cursor: "pointer",
            transition:
              "transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out",
            "&:hover": {
              backgroundColor: "#6f84ea",
              transform: "scale(1.03)",
              boxShadow: "0 6px 15px rgba(0, 0, 0, 0.3)",
            },
          }}
          onClick={() =>
            handleQuizClick(
              texts[0]?.unit, // Use the unit of the first text
              texts[0]?.grade // Use the grade of the first text
            )
          }
        >
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            Unit Progress Quiz
          </Typography>
        </Box>
      )}
    </Box>
  );
  
  

  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        background: "linear-gradient(to bottom, #f0f4ff, #e6f7ff)",
      }}
    >
      <Sidebar />
      <Box sx={{ flex: 1, p: 3, ml: "280px" }}>
        <AppBar
          position="static"
          sx={{
            backgroundColor: " #6f84ea",
            borderRadius: "10px",
            mb: 3,
          }}
        >
          <Toolbar>
            <Typography
              variant="h6"
              sx={{
                flexGrow: 1,
                fontWeight: "bold",
                fontSize: "1.5rem",
                color: "#FFF",
              }}
            >
              Learning Page
            </Typography>
          </Toolbar>
        </AppBar>
        {loading ? (
          <Box sx={{ textAlign: "center", mt: 5 }}>
            <CircularProgress />
          </Box>
        ) : (
          renderUnitsByGrade()
        )}
        {texts.length > 0 && renderTexts()}
      </Box>
    </Box>
  );
};

export default UnitsPage;
