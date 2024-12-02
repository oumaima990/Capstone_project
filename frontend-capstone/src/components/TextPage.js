import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  AppBar,
  Toolbar,
  Card,
  CardContent,
  Button,
} from "@mui/material";
import { useParams } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import axios from "axios";
import Question from "../components/Question";
import GlossaryCard from "../components/GlossaryCard";

const TextPage = () => {
  const { textId } = useParams(); // Get the text ID from the URL
  const [textData, setTextData] = useState({
    title: "Loading...",
    content: "Loading...",
    unit: null,
    grade: null,
    imageUrl: null,
  });

  const [studentId, setStudentId] = useState(null); // Dynamically manage student ID
  const [glossary, setGlossary] = useState(null); // For glossary popup
  const [question, setQuestion] = useState(null); // For question popup
  const [answerFeedback, setAnswerFeedback] = useState(null); // To display feedback after answer submission

  useEffect(() => {
    const fetchStudentSession = async () => {
      try {
        const studentSession = JSON.parse(sessionStorage.getItem("user"));

        if (studentSession && studentSession.id) {
          setStudentId(studentSession.id);
        } else {
          console.error("No student session found.");
        }
      } catch (error) {
        console.error("Error fetching student session:", error);
      }
    };

    fetchStudentSession();
  }, []);

  useEffect(() => {
    const fetchTextData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/knowledge/text/get_text_by_id/?id=${textId}`
        );
        if (response.data.length > 0) {
          const text = response.data[0];
          setTextData({
            title: text.title,
            content: text.content,
            unit: text.unit,
            grade: text.grade,
            imageUrl: text.image
              ? `http://127.0.0.1:8000/media/${text.image}`
              : null,
          });
        } else {
          setTextData({
            title: "Not Found",
            content: "The requested text could not be found.",
            unit: null,
            grade: null,
            imageUrl: null,
          });
        }
      } catch (err) {
        console.error("Error fetching text data:", err);
      }
    };

    fetchTextData();
  }, [textId]);

  const handleWordClick = async (word) => {
    try {
      if (!studentId) {
        console.error("Student ID not set.");
        return;
      }

      if (answerFeedback) setAnswerFeedback(null); // Reset feedback

      const payload = {
        text_id: textId,
        word,
        student_id: studentId,
      };

      const response = await axios.post(
        "http://127.0.0.1:8000/knowledge/knowledge-components/handle_click/",
        payload
      );

      if (response.data.action === "show_glossary") {
        setGlossary({
          node: response.data.glossary.node,
          sentence: response.data.glossary.Sentence,
          gloss: response.data.glossary.gloss,
          definition: response.data.glossary.definition,
        });
      } else if (response.data.action === "ask_question") {
        setQuestion({
          id: response.data.question_id,
          text: response.data.question_text,
        });
      }
    } catch (err) {
      console.error("Error handling word click:", err);
    }
  };

  const handleQuestionSubmit = async (answer) => {
    try {
      if (!studentId) {
        console.error("Student ID not set.");
        return;
      }

      const payload = {
        question_id: question.id,
        student_id: studentId,
        answer,
      };

      const response = await axios.post(
        "http://127.0.0.1:8000/knowledge/knowledge-components/update_probability/",
        payload
      );

      setAnswerFeedback({
        isCorrect: response.data.is_correct,
        probability: response.data.main_knowledge_component.p_know.toFixed(2),
      });

      setQuestion(null); // Reset question state
    } catch (err) {
      console.error("Error submitting answer:", err);
    }
  };

  const renderContentWithClickableWords = () => {
    return textData.content.split(" ").map((word, index) => (
      <span
        key={index}
        onClick={() => handleWordClick(word)}
        style={{ cursor: "pointer" }}
      >
        {word}
        {index < textData.content.split(" ").length - 1 ? " " : ""}
      </span>
    ));
  };

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "#f4f6f8" }}>
      {/* Sidebar */}
      <Box sx={{ width: "280px", flexShrink: 0 }}>
        <Sidebar />
      </Box>

      {/* Main Content */}
      <Box sx={{ flex: 1, padding: "24px" }}>
        {/* Unit Details Bar */}
        <AppBar
          position="static"
          sx={{
            backgroundColor: "#6f84ea",
            mb: 3,
            borderRadius: "10px",
            boxShadow: "0px 4px 15px rgba(0, 0, 0, 0.1)",
            padding: "16px",
          }}
        >
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <Typography
              variant="h6"
              sx={{
                fontWeight: "bold",
                color: "#fff",
                fontSize: "1.5rem",
                letterSpacing: "0.05em",
              }}
            >
              Unit Details
            </Typography>
            <Typography
              variant="subtitle1"
              sx={{
                color: "#fff",
                opacity: 0.9,
              }}
            >
              Grade: {textData.grade || "N/A"} | Unit: {textData.unit || "N/A"}
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Text Container */}
        <Card
          sx={{
            maxWidth: "900px",
            margin: "0 auto",
            backgroundColor: "#ffffff",
            borderRadius: "12px",
            boxShadow: "0 6px 15px rgba(0, 0, 0, 0.2)",
            overflow: "hidden",
            padding: "24px",
          }}
        >
          <Box
            sx={{
              backgroundColor: "#eef1f5",
              textAlign: "center",
              padding: "20px",
              borderRadius: "8px",
              mb: 3,
            }}
          >
            <Typography variant="h4" sx={{ fontWeight: "bold", color: "#001E3C" }}>
              {textData.title}
            </Typography>
          </Box>
          <CardContent>
            <Typography
              variant="body1"
              sx={{
                lineHeight: 1.8,
                color: "#333",
                fontSize: "1.1rem",
                mb: 3,
              }}
            >
              {renderContentWithClickableWords()}
            </Typography>

            {textData.imageUrl && (
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  mt: 3,
                }}
              >
                <img
                  src={textData.imageUrl}
                  alt={textData.title}
                  style={{
                    maxWidth: "100%",
                    maxHeight: "400px",
                    borderRadius: "8px",
                    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
                  }}
                />
              </Box>
            )}
          </CardContent>
        </Card>

        {/* Feedback Banner */}
        {answerFeedback && (
          <Box
            sx={{
              position: "fixed",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              zIndex: 1000,
            }}
          >
            <Card
              sx={{
                width: 400,
                padding: "16px",
                backgroundColor: answerFeedback.isCorrect ? "#d4edda" : "#f8d7da",
                color: answerFeedback.isCorrect ? "#155724" : "#721c24",
                textAlign: "center",
                boxShadow: "0 4px 10px rgba(0,0,0,0.2)",
              }}
            >
              <Typography variant="h6">
                {answerFeedback.isCorrect ? "Correct Answer!" : "Incorrect Answer"}
              </Typography>
              <Typography variant="body1">
                Updated Knowledge Probability: {answerFeedback.probability}
              </Typography>
              <Button
                onClick={() => setAnswerFeedback(null)} // Close the banner
                sx={{
                  mt: 2,
                  backgroundColor: answerFeedback.isCorrect ? "#155724" : "#721c24",
                  color: "white",
                  "&:hover": {
                    backgroundColor: answerFeedback.isCorrect ? "#138a51" : "#a71d2a",
                  },
                }}
              >
                Close
              </Button>
            </Card>
          </Box>
        )}
      </Box>

      {/* Glossary Component */}
      {glossary && (
        <GlossaryCard
          glossary={glossary}
          onClose={() => setGlossary(null)}
        />
      )}

      {/* Question Component */}
      <Question
        question={question}
        onClose={() => setQuestion(null)}
        onSubmit={handleQuestionSubmit}
      />
    </Box>
  );
};

export default TextPage;
