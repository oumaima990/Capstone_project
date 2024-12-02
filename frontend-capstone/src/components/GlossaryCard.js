import React from "react";
import { Card, CardContent, Typography, Box, Button } from "@mui/material";

const GlossaryCard = ({ glossary, onClose }) => {
  if (!glossary) return null;

  return (
    <Box
      sx={{
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        zIndex: 1000,
        width: 500,
      }}
    >
      <Card
        sx={{
          padding: "16px",
          backgroundColor: "#f8f9fa",
          boxShadow: "0 4px 10px rgba(0,0,0,0.2)",
          border: "2px solid gray", // Add a gray border to the card
          borderRadius: "8px", // Optional: To make the card look better
        }}
      >
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold", textAlign: "center" }}>
            Glossary
          </Typography>
          <Typography variant="body1" sx={{ mb: 2 }}>
            <strong>Gloss:</strong> {glossary.gloss || "N/A"}
          </Typography>
          <Typography variant="body1" sx={{ mb: 2 }}>
            <strong>Sentence:</strong> {glossary.sentence || "N/A"}
          </Typography>
          <Typography variant="body1">
            <strong>Definition:</strong> {glossary.definition || "N/A"}
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              mt: 2,
            }}
          >
            <Button
              onClick={onClose}
              sx={{
                backgroundColor: "#007bff",
                color: "white",
                "&:hover": {
                  backgroundColor: "#0056b3",
                },
              }}
            >
              Close
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default GlossaryCard;
