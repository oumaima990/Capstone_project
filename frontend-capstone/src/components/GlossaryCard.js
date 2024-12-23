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
        width: { xs: "90%", sm: 500 }, // Responsive width
      }}
    >
      <Card
        sx={{
          padding: "20px",
          backgroundColor: "#ffffff",
          boxShadow: "0 8px 20px rgba(0,0,0,0.1)", // Subtle shadow
          border: "1px solid #e0e0e0", // Soft border
          borderRadius: "12px", // Smooth corners
        }}
      >
        <CardContent>
          <Typography
            variant="h5"
            sx={{
              mb: 3,
              fontWeight: "bold",
              textAlign: "center",
              color: "#3f51b5", // Soft blue title
            }}
          >
            Glossary
          </Typography>
          <Typography
            variant="body1"
            sx={{ mb: 2, lineHeight: 1.6, fontSize: "1rem" }}
          >
            <strong style={{ color: "#333" }}>Gloss:</strong>{" "}
            {glossary.gloss || "N/A"}
          </Typography>
          <Typography
            variant="body1"
            sx={{ lineHeight: 1.6, fontSize: "1rem" }}
          >
            <strong style={{ color: "#333" }}>Definition:</strong>{" "}
            {glossary.definition || "N/A"}
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              mt: 3,
            }}
          >
            <Button
              onClick={onClose}
              sx={{
                backgroundColor: "#3f51b5",
                color: "#ffffff",
                padding: "10px 20px",
                fontSize: "1rem",
                fontWeight: "bold",
                borderRadius: "8px",
                textTransform: "none",
                "&:hover": {
                  backgroundColor: "#303f9f",
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
