import React, { useState } from "react";
import { Modal, Box, Typography, TextField, Button, Card } from "@mui/material";

const Question = ({ question, onClose, onSubmit }) => {
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const response = await onSubmit(answer);
    setResult(response);
  };

  if (!question) return null; // Ensure question is defined

  return (
    <Modal open={!!question} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          bgcolor: "background.paper",
          boxShadow: 24,
          p: 4,
          borderRadius: 2,
          maxWidth: 400,
          textAlign: "center",
        }}
      >
        {result ? (
          <Card
            sx={{
              p: 2,
              bgcolor: result.is_correct ? "green" : "red",
              color: "white",
              textAlign: "center",
              borderRadius: 2,
              mb: 2,
            }}
          >
            <Typography variant="h6">
              {result.is_correct ? "Correct Answer!" : "Incorrect Answer"}
            </Typography>
            <Typography variant="body1">
              {`Updated Knowledge Probability: ${result.main_knowledge_component.p_know.toFixed(
                2
              )}`}
            </Typography>
          </Card>
        ) : (
          <>
            <Typography variant="h6" sx={{ mb: 2 }}>
              {question?.text || "No question provided."}
            </Typography>

            {/* Multiple Choice Options */}
            {question.options && question.options.length > 0 ? (
              <Box>
                {question.options.map((option, index) => (
                  <Button
                    key={index}
                    variant="outlined"
                    sx={{ mt: 1, mx: 1 }}
                    onClick={() => setAnswer(option)}
                  >
                    {option}
                  </Button>
                ))}
              </Box>
            ) : (
              // Text Input for other question types
              <TextField
                fullWidth
                variant="outlined"
                label="Your Answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                sx={{ my: 2 }}
              />
            )}

            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              sx={{ mt: 2 }}
            >
              Submit Answer
            </Button>
          </>
        )}
      </Box>
    </Modal>
  );
};

export default Question;
