import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate from react-router-dom
import { Typography, Button, Container, Box } from "@mui/material";

const CloudBudgetAnalysisPage = () => {
  const navigate = useNavigate(); // Hook to navigate to different routes

  // Navigate to /basicform
  const handleBasicClick = () => {
    navigate("/form/basicform");
  };

  // Navigate to /advancedform
  const handleAdvancedClick = () => {
    navigate("/form/advancedform");
  };

  return (
    <Container>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Cloud Budget Analysis Form
        </Typography>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            mt: 4,
            gap: 4,
          }}
        >
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={handleBasicClick}
            sx={{
              borderRadius: "50%",
              width: 140,
              height: 140,
            }}
          >
            BASIC
          </Button>
          <Button
            variant="contained"
            color="secondary"
            size="large"
            onClick={handleAdvancedClick}
            sx={{
              borderRadius: "50%",
              width: 140,
              height: 140,
            }}
          >
            ADVANCED
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default CloudBudgetAnalysisPage;
