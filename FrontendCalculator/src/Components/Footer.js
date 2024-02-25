import React from "react";
import { Box, Link, Typography, Container, Grid } from "@mui/material";
import FacebookIcon from "@mui/icons-material/Facebook";
import TwitterIcon from "@mui/icons-material/Twitter";
import InstagramIcon from "@mui/icons-material/Instagram";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import MoneyPicture from "../Assets/home-banner-image.png";

const Footer = ({ style }) => {
  return (
    <Box
      sx={{
        backgroundColor: "#68a4cf",
        padding: "20px 0",
        color: "#000000",
        marginTop: style?.marginTop || 0, // Apply marginTop from props or default to 0
      }}
    >
      <Container maxWidth="lg">
        <Grid container justifyContent="center" alignItems="center" spacing={3}>
          <Grid
            item
            xs={12}
            container
            justifyContent="center"
            alignItems="center"
            style={{ paddingTop: "13px" }}
          >
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                color: "#000000",
                display: "flex",
                alignItems: "center",
                marginLeft: "5px",
                marginBottom: "-5px",
                marginRight: "10px",
              }} // Added marginRight to create space between icon and text
            >
              <img src={MoneyPicture} alt="Money" style={{ width: "50px", marginRight: "5px" }} />
              Budget Cloud
            </Typography>
          </Grid>
          <Grid
            item
            xs={12}
            container
            justifyContent="center"
            spacing={2}
            sx={{ marginBottom: "-15px" }}
          >
            <Link href="#" sx={{ color: "#000000", mx: 2, fontSize: "19px" }}>
              <FacebookIcon sx={{ fontSize: "inherit" }} />
            </Link>
            <Link href="#" sx={{ color: "#000000", mx: 2, fontSize: "19px" }}>
              <TwitterIcon sx={{ fontSize: "inherit" }} />
            </Link>
            <Link href="#" sx={{ color: "#000000", mx: 2, fontSize: "19px" }}>
              <InstagramIcon sx={{ fontSize: "inherit" }} />
            </Link>
            <Link href="#" sx={{ color: "#000000", mx: 2, fontSize: "19px" }}>
              <LinkedInIcon sx={{ fontSize: "inherit" }} />
            </Link>
          </Grid>
        </Grid>
        <Typography
          variant="body2"
          align="center"
          sx={{ pt: 3, color: "#000000", fontSize: "11px" }}
        >
          © 2024 Budget Cloud. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
