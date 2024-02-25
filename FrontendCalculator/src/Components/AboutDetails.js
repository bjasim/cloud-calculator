import React from "react";
import { Container, Typography, Grid } from "@mui/material";
import school from "../Assets/conestoga.jpg"; // Import your bug image

const AboutUs = () => {
  return (
    <Container>
      <Grid container spacing={4} justifyContent="center">
        <Grid item xs={12}>
          <img
            src={school}
            alt="Bug"
            style={{ width: "90%", maxWidth: "800px", display: "block", margin: "20px auto" }}
          />
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            About Us
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1" style={{ marginBottom: "2px" }}>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum
            has been the industry's standard dummy text ever since the 1500s, when an unknown
            printer took a galley of type and scrambled it to make a type specimen book. It has
            survived not only five centuries, but also the leap into electronic typesetting,
            remaining essentially unchanged. It was popularised in the 1960s with the release of
            Letraset sheets containing Lorem Ipsum passages, and more recently with desktop
            publishing software like Aldus PageMaker including versions of Lorem Ipsum.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1" style={{ marginBottom: "2px" }}>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum
            has been the industry's standard dummy text ever since the 1500s, when an unknown
            printer took a galley of type and scrambled it to make a type specimen book. It has
            survived not only five centuries, but also the leap into electronic typesetting,
            remaining essentially unchanged. It was popularised in the 1960s with the release of
            Letraset sheets containing Lorem Ipsum passages, and more recently with desktop
            publishing software like Aldus PageMaker including versions of Lorem Ipsum.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1" style={{ marginBottom: "5rem" }}>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum
            has been the industry's standard dummy text ever since the 1500s, when an unknown
            printer took a galley of type and scrambled it to make a type specimen book. It has
            survived not only five centuries, but also the leap into electronic typesetting,
            remaining essentially unchanged. It was popularised in the 1960s with the release of
            Letraset sheets containing Lorem Ipsum passages, and more recently with desktop
            publishing software like Aldus PageMaker including versions of Lorem Ipsum.
          </Typography>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AboutUs;
