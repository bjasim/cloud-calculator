
import React from "react";
import { Container, Typography, Grid } from "@mui/material";
import school from "../Assets/home-banner-image.png"; // Import your bug image

const ContactPage = () => {
  return (
    <Container>
      <Grid container spacing={4} justifyContent="center">
        <Grid item xs={12}>
          <img
            src={school}
            alt="Bug"
            style={{ width: "100%", maxWidth: "250px", display: "block", margin: "20px auto", marginBottom: "-60px" }}
          />
        </Grid> 
        <Grid item xs={12}>
        </Grid>
          <Typography variant="h3" gutterBottom>
          Navigating the Cloud
          </Typography>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Introduction to Cloud Computing
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "2px" }}>
          &emsp; Cloud computing is like renting technology services — computing power, storage, and more — over the internet. It lets you access and store data without owning physical hardware. Think of it as subscribing to a streaming service instead of buying DVDs.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom  style={{ marginBottom: "2rem" }}>
              Understanding Cloud Pricing: Pay-As-You-Go
          </Typography>
          <Typography variant="h5" gutterBottom >
          The Flexibility of Cloud Costs          
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "2px" }}>
          &emsp; Unlike traditional IT where you invest heavily upfront in servers and infrastructure, the cloud operates on a pay-as-you-go model. This means you only pay for the computing resources you use, similar to how a utility bill works for electricity or water.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
          Scalability: Match Demand with Supply
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "0rem" }}>
          &emsp; One of the cloud's biggest advantages is scalability. You can easily increase your computing resources during peak times and decrease them when they're not needed, ensuring efficient use of your budget.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom  style={{ marginBottom: "2rem" }}>
          On-Premises vs. Cloud: The Technical Perspective
          </Typography>
          <Typography variant="h5" gutterBottom>
          On-Premises Explained          </Typography>
          <Typography variant="body1" style={{ marginBottom: "1rem" }}>
          &emsp; Choosing on-prem solutions means you keep and look after your IT setup right where your business is. You get complete control over your data and equipment but need to be ready for a big initial investment and regular costs to keep everything running smoothly. A basic setup with decent quality servers usually falls between $5,000 and $15,000 each. Adding a reliable backup system adds on about $2,000 more. Also, there are software licenses, Microsoft for example, can cost roughly $1,500 per server, plus more fees for each user and special software like Microsoft SQL. Starting with 2 to 3 servers, the initial investment could be around $25,000, but remember, the price must be adjusted to your specific needs.
          </Typography>
          <Typography variant="h5" gutterBottom>
          Advantages of Cloud Solutions          
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "0rem" }}>
          &emsp; Cloud computing removes the need for physical hardware, reducing capital expenditure. It offers robust scalability, improved disaster recovery, and flexible work practices since services can be accessed from anywhere, anytime.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom  style={{ marginBottom: "2rem" }}>
          Unveiling Hidden Costs
          </Typography>
          <Typography variant="h5" gutterBottom>
          Potential Overlooked Expenses          </Typography>
          <Typography variant="body1" style={{ marginBottom: "1rem" }}>
          &emsp; When migrating to or scaling within the cloud, be mindful of hidden costs such as data egress fees, storage retrieval costs, and support services. Planning and utilizing cost management tools provided by cloud services can mitigate unexpected expenses.
          </Typography>
          <Typography variant="h5" gutterBottom>
          Migrating to the Cloud          
          </Typography>
          <Typography variant="body1" style={{ marginBottom: "5rem" }}>
          &emsp; Transitioning to the cloud requires careful planning. Assess your current IT infrastructure, determine what you need in the cloud, and choose a provider that fits your needs. Many cloud providers offer migration tools to simplify the process.
          </Typography>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ContactPage;
