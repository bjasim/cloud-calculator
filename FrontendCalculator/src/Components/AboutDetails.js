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
            style={{ width: "60%", maxWidth: "800px", display: "block", margin: "20px auto" }}
          />
        </Grid> 
        <Grid item xs={12}>
        </Grid>
          <Typography variant="h4" gutterBottom>
            About Us
          </Typography>
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
            Introduction
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "2px" }}>
          Welcome to BudgetCloud! We're a team of Software Engineering students from Conestoga who
          decided to make it easier for everyone to understand how much cloud services could cost. 
          We're here to help you figure out the best deals for cloud computing, whether it's for storing 
          your files or running your website.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
            Our Approach
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "2px" }}>
            We know that looking into cloud services can get really complicated, especially with all the options out there. That's why we've made two ways for you to find out what you might need to pay: a Basic Form and an Advanced Form.
            Basic Form: This one's for you if you're not too familiar with the cloud. Just answer some simple questions about what you need, like expected users and complex or basic computing, and we'll show you some options that fit your needs.
            Advanced Form: If you know what you're looking for and want more control over the details, this form lets you be more specific. It's perfect for those who know their way around cloud services.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
           Budget Cloud
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "5rem" }}>
          BudgetCloud is for everyone - from small business owners who are looking to move their stuff online, to 
          startups that need to handle a lot of users and have a strict budget, or even developers looking for a 
          good deal on storage. At BudgetCloud, we're all about making sure you have the information you need to 
          make smart choices about cloud services. We compare prices and options for you, so you can focus on what's
          best for your project or business.
          </Typography>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AboutUs;
