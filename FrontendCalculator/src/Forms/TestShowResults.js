import React from "react";
import { Box, Card, CardContent, Typography, CardMedia } from "@mui/material";
import GoogleCloudLogo from "../Assets/google.png";
import AwsLogo from "../Assets/aws.png";
import AzureLogo from "../Assets/azure.png";
import OracleLogo from "../Assets/oracle.jpg";

const TestResults = () => {
  const logos = {
    "Microsoft Azure": AzureLogo,
    AWS: AwsLogo,
    "Google Cloud": GoogleCloudLogo,
    Oracle: OracleLogo,
  };

  const names = Object.keys(logos);

  const plans = [
    {
      monthly: "$320",
      annual: "$3200",
      provider: "Microsoft Azure",
      compute: { name: "B1ls", cpu: "2 vCPU", ram: "4 GiB", price: "$110" },
      storage: { name: "Blob Storage", size: "100GB", price: "$55" },
      database: { name: "MySQL", size: "1 GB", price: "$0.25" },
      networking: { name: "VNET", speed: "1 Gbps", price: "$75" },
    },
    {
      monthly: "$350",
      annual: "$3500",
      provider: "AWS",
      compute: { name: "t3.nano", cpu: "2 vCPU", ram: "4 GiB", price: "$120" },
      storage: { name: "S3 Standard", size: "100GB", price: "$60" },
      database: { name: "MySQL", size: "1 GB", price: "$0.25" },
      networking: { name: "VPC", speed: "1 Gbps", price: "$80" },
    },
    {
      monthly: "$300",
      annual: "$3000",
      provider: "Google Cloud",
      compute: { name: "t4g.nano", cpu: "2 vCPU", ram: "4 GiB", price: "$100" },
      storage: { name: "Standard HDD", size: "100GB", price: "$50" },
      database: { name: "MySQL", size: "1 GB", price: "$0.25" },
      networking: { name: "VPC", speed: "1 Gbps", price: "$70" },
    },
    {
      monthly: "$320",
      annual: "$3200",
      provider: "Oracle",
      compute: { name: "E2.1.Micro", cpu: "2 vCPU", ram: "4 GiB", price: "$110" },
      storage: { name: "Object Storage", size: "100GB", price: "$55" },
      database: { name: "MySQL", size: "1 GB", price: "$0.25" },
      networking: { name: "VCN", speed: "1 Gbps", price: "$75" },
    },
  ];

  return (
    <Box sx={{ display: "flex", justifyContent: "center", p: 4, flexWrap: "wrap" }}>
      {names.map((name, index) => {
        const plan = plans.find((plan) => plan.provider === name);
        return (
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
                image={logos[name]}
                alt={`${name} logo`}
              />
            </Box>
            <CardContent sx={{ flexGrow: 1, paddingTop: "0px" }}>
              <Typography gutterBottom variant="h5" component="div" align="center">
                {name}
              </Typography>
              <div style={{ marginBottom: "15px", fontSize: "1.5rem", textAlign: "center" }}>
                Price/Month
              </div>
              {plan ? (
                <div>
                  <span style={{ fontSize: "1.2rem" }}>Compute:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>
                    {plan.compute ? plan.compute.price : "-"}
                  </span>{" "}
                  <br />
                  <span style={{ fontSize: "1.1rem" }}>
                    {plan.compute ? `${plan.compute.name} - ${plan.compute.cpu}` : "-"}
                  </span>{" "}
                  <span style={{ fontSize: "1.1rem" }}>
                    {plan.compute ? plan.compute.ram : "-"}
                  </span>
                  <div>==================</div>
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Storage:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>
                    {plan.storage ? plan.storage.price : "-"}
                  </span>{" "}
                  <br />
                  <span style={{ fontSize: "1.1rem" }}>
                    {plan.storage ? `${plan.storage.name} - ${plan.storage.size}` : "-"}
                  </span>
                  <div>==================</div>
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Database:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>
                    {plan.database ? plan.database.price : "-"}
                  </span>{" "}
                  <br />
                  <span style={{ fontSize: "1.1rem" }}>
                    {plan.database ? `${plan.database.name} - ${plan.database.size}` : "-"}
                  </span>
                  <div>==================</div>
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Networking:</span>{" "}
                  <span style={{ fontSize: "1.2rem" }}>
                    {plan.networking ? plan.networking.price : "-"}
                  </span>{" "}
                  <br />
                  <span style={{ fontSize: "1.1rem" }}>
                    {plan.networking ? `${plan.networking.name} - ${plan.networking.speed}` : "-"}
                  </span>
                </div>
              ) : (
                <Typography align="center">No data available</Typography>
              )}
            </CardContent>
            {plan && (
              <CardContent>
                <div style={{ fontSize: "1.3rem" }}>
                  ============== <br />
                  <span style={{ fontSize: "1.2rem" }}>
                    Monthly Total: {plan.monthly || "-"}
                  </span>{" "}
                  <br />
                  <span style={{ fontSize: "1.2rem" }}>Annual Total: {plan.annual || "-"}</span>
                </div>
              </CardContent>
            )}
          </Card>
        );
      })}
    </Box>
  );
};

export default TestResults;
