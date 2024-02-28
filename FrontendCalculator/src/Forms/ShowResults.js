import React from "react";
import { Box, Card, CardContent, Typography, CardMedia } from "@mui/material";
import GoogleCloudLogo from "../Assets/google.png";
import AwsLogo from "../Assets/aws.png";
import AzureLogo from "../Assets/azure.png";
import OracleLogo from "../Assets/oracle.jpg";

const RecommendedPlans = () => {
  const plans = [
    {
      name: "Google Cloud",
      logo: GoogleCloudLogo,
      monthly: "$300",
      annual: "$3000",
      compute: { instance: "t4g.nano - 2 vCPU 4 GiB ", price: "$100" }, // Add compute pricing
      storage: { instance: "Standard HDD - 100GB", price: "$50" }, // Add storage pricing
      database: { instance: "MySQL - 1 GB ", price: "$0.25" }, // Add database pricing
      networking: { instance: "VPC - 1 Gbps", price: "$70" }, // Add networking pricing
    },
    {
      name: "AWS",
      logo: AwsLogo,
      monthly: "$350",
      annual: "$3500",
      compute: { instance: "t3.nano - 2 vCPU 4 GiB ", price: "$120" }, // Add compute pricing
      storage: { instance: "S3 Standard - 100GB", price: "$60" }, // Add storage pricing
      database: { instance: "MySQL - 1 GB ", price: "$0.25" }, // Add database pricing
      networking: { instance: "VPC - 1 Gbps", price: "$80" }, // Add networking pricing
    },
    {
      name: "Microsoft Azure",
      logo: AzureLogo,
      monthly: "$320",
      annual: "$3200",
      compute: { instance: "B1ls - 2 vCPU 4 GiB ", price: "$110" }, // Add compute pricing
      storage: { instance: "Blob Storage - 100GB", price: "$55" }, // Add storage pricing
      database: { instance: "MySQL - 1 GB ", price: "$0.25" }, // Add database pricing
      networking: { instance: "VNET - 1 Gbps", price: "$75" }, // Add networking pricing
    },
    {
      name: "Oracle",
      logo: OracleLogo,
      monthly: "$320",
      annual: "$3200",
      compute: { instance: "E2.1.Micro - 2 vCPU 4 GiB ", price: "$110" }, // Add compute pricing
      storage: { instance: "Object Storage - 100GB", price: "$55" }, // Add storage pricing
      database: { instance: "MySQL - 1 GB ", price: "$0.25" }, // Add database pricing
      networking: { instance: "VCN - 1 Gbps", price: "$75" }, // Add networking pricing
    },
  ];

  return (
    <Box sx={{ display: "flex", justifyContent: "center", p: 4, flexWrap: "wrap" }}>
      {plans.map((plan, index) => (
        <Card key={index} sx={{ maxWidth: 345, m: 2, display: "flex", flexDirection: "column" }}>
          <Box
            sx={{
              height: 200,
              width: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "#fff",
            }}
          >
            <CardMedia
              component="img"
              sx={{
                height: "auto",
                width: "auto",
                maxHeight: 140,
                maxWidth: 400,
              }}
              image={plan.logo}
              alt={`${plan.name} logo`}
            />
          </Box>
          <CardContent sx={{ flexGrow: 1, paddingTop: "0px" }}>
            <Typography
              gutterBottom
              variant="h5"
              component="div"
              align="center"
              sx={{
                paddingTop: "0px",
              }}
            >
              {plan.name}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              fontWeight="bold"
              sx={{
                marginTop: "20px",
              }}
            >
              <div>
                <h2 style={{ textAlign: "center", marginBottom: "15px", fontSize: "1.5rem" }}>
                  Price/Month
                </h2>{" "}
                {/* Center align and increase font size */}
                <div>
                  <span style={{ fontSize: "1.2rem" }}>Compute:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>{plan.compute.price}</span> <br />
                  <span style={{ fontSize: "1.1rem" }}>{plan.compute.instance}</span>
                  <div>==================</div>
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Storage:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>{plan.storage.price}</span> <br />
                  <span style={{ fontSize: "1.1rem" }}>{plan.storage.instance}</span>
                  <div>==================</div>
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Database:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>{plan.database.price}</span> <br />
                  <span style={{ fontSize: "1.1rem" }}>{plan.database.instance}</span>
                  <div>==================</div>
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Networking:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>{plan.networking.price}</span> <br />
                  <span style={{ fontSize: "1.1rem" }}>{plan.networking.instance}</span>
                  <br />
                </div>
              </div>
              <div style={{ marginBottom: "5px", marginTop: "15px" }}>==================</div>
              <span style={{ fontSize: "1.2rem" }}>Monthly Total: {plan.monthly}</span> <br />
              <span style={{ fontSize: "1.2rem" }}>Annual Total: {plan.annual}</span>
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default RecommendedPlans;
