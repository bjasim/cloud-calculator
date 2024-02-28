import React from "react";
import { Container, Typography, Grid, Avatar, Box } from "@mui/material";
import { Star, StarHalf } from "@mui/icons-material";

const Testimonials = () => {
  return (
    <Container sx={{ py: 5 }}>
      <Grid container spacing={3} justifyContent="center">
        <Grid item xs={12}>
          <Typography variant="h4" align="center" gutterBottom>
            Testimonials
          </Typography>
          <Typography variant="body1" align="center" sx={{ mb: 4 }}>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Fugit, error amet numquam iure
            provident voluptate esse quasi, veritatis totam voluptas nostrum quisquam eum porro a
            pariatur veniam.
          </Typography>
        </Grid>
        <Grid item xs={12} md={4}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 5 }}>
            <Avatar
              alt="Maria Smantha"
              src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(1).webp"
              sx={{ width: 150, height: 150, mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              Maria Smantha
            </Typography>
            <Typography variant="subtitle1" gutterBottom color="primary">
              Web Developer
            </Typography>
            <Typography variant="body1" align="center" sx={{ px: { xs: 2, xl: 3 }, mb: 2 }}>
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <StarHalf sx={{ color: "warning.main" }} />
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quod eos id officiis hic
              tenetur quae quaerat ad velit ab hic tenetur.
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={12} md={4}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 5 }}>
            <Avatar
              alt="Lisa Cudrow"
              src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(2).webp"
              sx={{ width: 150, height: 150, mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              Lisa Cudrow
            </Typography>
            <Typography variant="subtitle1" gutterBottom color="primary">
              Graphic Designer
            </Typography>
            <Typography variant="body1" align="center" sx={{ px: { xs: 2, xl: 3 }, mb: 2 }}>
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit
              laboriosam, nisi ut aliquid commodi.
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={12} md={4}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 5 }}>
            <Avatar
              alt="John Smith"
              src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(9).webp"
              sx={{ width: 150, height: 150, mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              John Smith
            </Typography>
            <Typography variant="subtitle1" gutterBottom color="primary">
              Marketing Specialist
            </Typography>
            <Typography variant="body1" align="center" sx={{ px: { xs: 2, xl: 3 }, mb: 2 }}>
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium
              voluptatum deleniti atque corrupti.
            </Typography>
          </Box>
        </Grid>
        {/* Additional Testimonials */}
        <Grid item xs={12} md={4}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 5 }}>
            <Avatar
              alt="Emma Watson"
              src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(10).webp"
              sx={{ width: 150, height: 150, mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              Emma Watson
            </Typography>
            <Typography variant="subtitle1" gutterBottom color="primary">
              Software Engineer
            </Typography>
            <Typography variant="body1" align="center" sx={{ px: { xs: 2, xl: 3 }, mb: 2 }}>
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <StarHalf sx={{ color: "warning.main" }} />
              <StarHalf sx={{ color: "warning.main" }} />
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quod eos id officiis hic
              tenetur quae quaerat ad velit ab hic tenetur.
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={12} md={4}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 5 }}>
            <Avatar
              alt="David Beckham"
              src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(11).webp"
              sx={{ width: 150, height: 150, mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              David Beckham
            </Typography>
            <Typography variant="subtitle1" gutterBottom color="primary">
              UX Designer
            </Typography>
            <Typography variant="body1" align="center" sx={{ px: { xs: 2, xl: 3 }, mb: 2 }}>
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit
              laboriosam, nisi ut aliquid commodi.
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={12} md={4}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 5 }}>
            <Avatar
              alt="Jennifer Lawrence"
              src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(12).webp"
              sx={{ width: 150, height: 150, mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              Jennifer Lawrence
            </Typography>
            <Typography variant="subtitle1" gutterBottom color="primary">
              Data Analyst
            </Typography>
            <Typography variant="body1" align="center" sx={{ px: { xs: 2, xl: 3 }, mb: 2 }}>
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <Star sx={{ color: "warning.main" }} />
              <StarHalf sx={{ color: "warning.main" }} />
              At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium
              voluptatum deleniti atque corrupti.
            </Typography>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Testimonials;
