import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Paper,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField,
  CircularProgress,
} from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import Sidebar from "./Sidebar"; // Import the Sidebar component

const QuizPage = () => {
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState(null); // To store quiz results
  const navigate = useNavigate();
  const location = useLocation();

  // Extract grade and unit from query parameters
  const searchParams = new URLSearchParams(location.search);
  const grade = searchParams.get("grade");
  const unit = searchParams.get("unit");

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/knowledge/quiz/generate-quiz/?grade=${grade}&unit=${unit}&num_questions=5`
        );
        setQuestions(response.data);
      } catch (error) {
        console.error("Error fetching quiz questions:", error);
        alert(
          `An error occurred while fetching questions: ${
            error.response?.data?.error || "Please try again."
          }`
        );
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [grade, unit]);

  const handleResponseChange = (questionId, value) => {
    setResponses({
      ...responses,
      [questionId]: value,
    });
  };

  const handleSubmit = async () => {
    setSubmitting(true);

    const studentSession = JSON.parse(sessionStorage.getItem("user"));
    const studentId = studentSession?.id;

    if (!studentId) {
      alert("Student ID is not available.");
      setSubmitting(false);
      return;
    }

    const allAnswered = questions.every(
      (q) => responses[q.id] !== undefined && responses[q.id] !== ""
    );

    if (!allAnswered) {
      alert("Please answer all questions before submitting.");
      setSubmitting(false);
      return;
    }

    const formattedResponses = Object.keys(responses).map((questionId) => ({
      question_id: questionId,
      student_answer: responses[questionId].trim(),
    }));

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/knowledge/knowledge-components/submit-quiz/",
        {
          student_id: studentId,
          grade_order: grade,
          unit_order: unit,
          responses: formattedResponses,
        }
      );

      setResults(response.data); // Store the results for display
    } catch (error) {
      console.error("Error submitting quiz:", error);
      alert(
        `An error occurred while submitting the quiz: ${
          error.response?.data?.error || "Please try again."
        }`
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (results) {
    // Display results
    return (
      <Box
        sx={{
          maxWidth: "800px",
          margin: "0 auto",
          p: 3,
          textAlign: "center",
        }}
      >
        <Typography variant="h4" sx={{ mb: 3, fontWeight: "bold", color: "#001E3C" }}>
          Quiz Results
        </Typography>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Score: {results.score}%
        </Typography>
        <Typography variant="h6" sx={{ mb: 2 }}>
          {results.passed ? "Congratulations! You passed the quiz." : "You did not pass the quiz. Please try again."}
        </Typography>
        {results.next_unit_unlocked && (
          <Typography variant="h6" sx={{ mb: 3 }}>
            New Unit Unlocked: {results.next_unit_unlocked}
          </Typography>
        )}

        <Typography variant="h5" sx={{ mb: 3, fontWeight: "bold", color: "#001E3C" }}>
          Answers Review
        </Typography>
        {questions.map((question, index) => (
          <Paper
            key={question.id}
            elevation={3}
            sx={{
              p: 3,
              mb: 3,
              backgroundColor: "#ffffff",
              borderRadius: "10px",
              boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)",
            }}
          >
            <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold", color: "#001E3C" }}>
              {index + 1}. {question.question}
            </Typography>
            <Typography variant="body1" sx={{ color: "#001E3C" }}>
              Your Answer: {responses[question.id]}
            </Typography>
            <Typography variant="body1" sx={{ color: "#4CAF50" }}>
              Correct Answer: {results.correct_answers[question.id]?.correct_answer || "N/A"}
            </Typography>
            <Typography
              variant="body2"
              sx={{
                color: results.correct_answers[question.id]?.is_correct ? "#4CAF50" : "#F44336",
              }}
            >
              {results.correct_answers[question.id]?.is_correct ? "Correct" : "Incorrect"}
            </Typography>
          </Paper>
        ))}
        <Button
          variant="contained"
          sx={{
            mt: 3,
            backgroundColor: "#4CAF50",
            color: "#fff",
            fontWeight: "bold",
            textTransform: "none",
            width: "100%",
            "&:hover": {
              backgroundColor: "#45A049",
            },
          }}
          onClick={() => navigate("/units")}
        >
          Back to Units
        </Button>
      </Box>
    );
  }

  if (questions.length === 0) {
    return (
      <Box
        sx={{
          maxWidth: "800px",
          margin: "0 auto",
          p: 3,
          textAlign: "center",
        }}
      >
        <Typography
          variant="h6"
          sx={{
            color: "#001E3C",
            fontWeight: "bold",
          }}
        >
          No questions available for this quiz.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      {/* Render Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <Box
        sx={{
          flex: 1,
          marginLeft: "250px", // Adjust for the sidebar width
          padding: "2rem",
          overflowY: "auto",
        }}
      >
        <Typography
          variant="h4"
          sx={{
            mb: 3,
            fontWeight: "bold",
            color: "#001E3C",
            textAlign: "center",
          }}
        >
          Quiz for Grade {grade}, Unit {unit}
        </Typography>

        {questions.map((question, index) => (
          <Paper
            key={question.id}
            elevation={3}
            sx={{
              p: 3,
              mb: 3,
              backgroundColor: "linear-gradient(to bottom, #f0f4ff, #e6f7ff)",
              borderRadius: "10px",
              boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)",
            }}
          >
            <Typography
              variant="h6"
              sx={{ mb: 2, fontWeight: "bold", color: "#001E3C" }}
            >
              {index + 1}. {question.question}
            </Typography>

            {question.type === "multiple_choice" ? (
              <RadioGroup
                name={`question-${question.id}`}
                value={responses[question.id] || ""}
                onChange={(e) =>
                  handleResponseChange(question.id, e.target.value)
                }
              >
                {question.options.map((option, idx) => (
                  <FormControlLabel
                    key={idx}
                    value={option}
                    control={<Radio />}
                    label={option}
                  />
                ))}
              </RadioGroup>
            ) : (
              <TextField
                variant="outlined"
                fullWidth
                placeholder="Type your answer here..."
                value={responses[question.id] || ""}
                onChange={(e) =>
                  handleResponseChange(question.id, e.target.value)
                }
              />
            )}
          </Paper>
        ))}

        <Button
          variant="contained"
          sx={{
            mt: 3,
            backgroundColor: "#4CAF50",
            color: "#720072",
            fontWeight: "bold",
            textTransform: "none",
            width: "100%",
            "&:hover": {
              backgroundColor: "#45A049",
            },
          }}
          onClick={handleSubmit}
          disabled={submitting}
        >
          {submitting ? "Submitting..." : "Submit Quiz"}
        </Button>
      </Box>
    </Box>
  );
};

export default QuizPage;
