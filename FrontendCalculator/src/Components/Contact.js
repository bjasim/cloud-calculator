import React, { useState } from "react";
import { Container, Typography, TextField, Button, Box, Grid } from "@mui/material";
import picture1 from "../Assets/home-banner-background.png";
import picture2 from "../Assets/about-background-image.png";

const ContactPage = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h3" align="center" gutterBottom style={{ marginTop: "25px" }}>
        Contact Us
      </Typography>
      <Typography variant="body1" align="center" paragraph>
        We'd love to hear from you! Please fill out the form below to get in touch with us.
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} style={{ position: "relative" }}>
          <img
            src={picture1}
            alt="Descriptive Alt Text"
            style={{ width: "100%", height: "auto" }}
          />
          <img
            src={picture2}
            alt="Descriptive Alt Text"
            style={{
              position: "absolute",
              top: 0,
              left: "-150px", // Move picture2 50px to the left
              width: "calc(80% + 50px)", // Make picture2 50px smaller and adjust its width
              height: "auto",
              objectFit: "cover",
            }}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              maxWidth: 600,
              mx: "auto",
              p: 2,
              border: "2px solid  #000000",
              borderRadius: "12px",
              boxShadow: 1,
            }}
          >
            <Typography variant="h4" align="center" mb={2}></Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                label="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                margin="normal"
                required
                type="email"
              />
              <TextField
                fullWidth
                label="Message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                margin="normal"
                required
                multiline
                rows={7}
              />
              <Button
                fullWidth
                type="submit"
                sx={{
                  mt: 2,
                  backgroundColor: "#000",
                  color: "#fff",
                  "&:hover": {
                    backgroundColor: "#111",
                  },
                }}
              >
                Submit
              </Button>
            </form>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ContactPage;
