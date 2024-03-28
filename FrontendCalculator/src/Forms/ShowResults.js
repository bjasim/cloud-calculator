import React, { useEffect, useState } from "react";
import { Box, Card, CardContent, Typography, CardMedia, Tooltip} from "@mui/material";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import GoogleCloudLogo from "../Assets/google.png";
import AwsLogo from "../Assets/aws.png";
import AzureLogo from "../Assets/azure.png";
import OracleLogo from "../Assets/oracle.jpg";

const RecommendedPlans = ({ responseData }) => {
  const logos = {
    "Microsoft Azure": AzureLogo,
    AWS: AwsLogo,
    "Google Cloud": GoogleCloudLogo,
    Oracle: OracleLogo,
  };
  const [azureCreatedAt, setAzureCreatedAt] = useState("");
  const [loading, setLoading] = useState(true);
  const [plans, setPlans] = useState([]);

  useEffect(() => {
    if (responseData) {
      console.log("Received Response Data:", responseData);

      let newPlans = [];
      let azureCreatedAtTemp = "";
      if (responseData.AWS) {
        newPlans.push({ provider: "AWS", ...responseData.AWS });
      }
      if (responseData.Azure) {
        newPlans.push({ provider: "Microsoft Azure", ...responseData.Azure });
        const azureServices = responseData.Azure;
        azureCreatedAtTemp =
          azureServices.networking?.created_at ||
          azureServices.storage?.created_at ||
          azureServices.database?.created_at ||
          azureServices.compute?.created_at;
      }
      if (responseData.Google) {
        newPlans.push({ provider: "Google Cloud", ...responseData.Google });
      }
      if (responseData.Oracle) {
        newPlans.push({ provider: "Oracle", ...responseData.Oracle });
      }

      console.log("New Plans:", newPlans);
      setPlans(newPlans);
      setLoading(false);
      setAzureCreatedAt(azureCreatedAtTemp);
    }
  }, [responseData]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
  <Box sx={{ p: 4 }}>
      <Box sx={{ textAlign: 'center', mt: 4, position: 'relative', zIndex: 2 }}>
        <Tooltip title="- - - * All prices in USD * - - - * 720 hours monthly * - - -">
          <HelpOutlineIcon sx={{ cursor: 'pointer', fontSize: 24 }} />
        </Tooltip>
        <Typography variant="h6" gutterBottom>
          Data Updated On: {azureCreatedAt}
        </Typography>
      </Box>
    <Box sx={{ display: "flex", justifyContent: "center", p: 4, flexWrap: "wrap" }}>

      {plans.map((plan, index) => {
        const name = plan.provider;
        return (
          <Card key={index} sx={{ maxWidth: 250, m: 2, display: "flex", flexDirection: "column" }}>
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
                Price
              </div>
              {plan ? (
                <div>
                  <div style={{ fontSize: "1.2rem", textAlign: "center" }}>
                    <strong>Compute</strong>
                  </div>
                  <div style={{ textAlign: "center" }}>
                    {plan.compute ? (
                      <>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>Name: {plan.compute.name}</span>
                        </div>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>Sku: {plan.compute.sku}</span>
                        </div>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>
                            {plan.compute.cpu} -{plan.compute.memory}
                          </span>
                        </div>
                        <div style={{ fontSize: "1.2rem", textAlign: "left" }}>
                          Price/Monthly: ${plan.compute.unit_price}
                        </div>
                      </>
                    ) : (
                      <div>
                        <span style={{ fontSize: "1.1rem" }}>CPU: Not Available</span>
                      </div>
                    )}
                  </div>
                  <div>==================</div>
                  <div style={{ fontSize: "1.2rem", textAlign: "center" }}>
                    <strong>Storage</strong>
                  </div>
                  <div style={{ textAlign: "center" }}>
                    {plan.storage ? (
                      <>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>
                            Name:
                            {plan.storage.name}
                          </span>{" "}
                        </div>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>Sku: {plan.storage.sku}</span>
                        </div>
                        <div style={{ fontSize: "1.2rem", textAlign: "left" }}>
                          Price/Monthly: ${plan.storage.unit_price}
                        </div>
                      </>
                    ) : (
                      <div style={{ textAlign: "left" }}>
                        <span style={{ fontSize: "1.1rem" }}>Storage: Not Available</span>
                      </div>
                    )}
                  </div>
                  <div>==================</div>
                  <div style={{ fontSize: "1.2rem", textAlign: "center" }}>
                    <strong>Database</strong>
                  </div>
                  <div style={{ textAlign: "center" }}>
                    {plan.database && plan.database.unit_price ? (
                      <>
                        <div style={{ textAlign: "center" }}>
                          <div style={{ textAlign: "left" }}>
                            <span style={{ fontSize: "1.1rem" }}>Name: {plan.database.name}</span>{" "}
                          </div>
                          <div style={{ textAlign: "left" }}>
                            <span style={{ fontSize: "1.1rem" }}>Sku: {plan.database.sku}</span>{" "}
                          </div>
                          <div style={{ fontSize: "1.2rem", textAlign: "left" }}>
                            Price/Monthly: ${plan.database.unit_price}
                          </div>
                        </div>
                      </>
                    ) : (
                      <div style={{ fontSize: "1.2rem", textAlign: "center" }}>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>Database: Not Available</span>
                        </div>
                      </div>
                    )}
                  </div>
                  <div>==================</div>
                  <div style={{ fontSize: "1.2rem", textAlign: "center" }}>
                    <strong>Networking</strong>
                  </div>
                  <div style={{ textAlign: "center" }}>
                    {plan.networking ? (
                      <>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>
                            Name:
                            {plan.networking.name}
                          </span>{" "}
                        </div>
                        <div style={{ textAlign: "left" }}>
                          <span style={{ fontSize: "1.1rem" }}>Sku: {plan.networking.sku}</span>
                        </div>
                        <div style={{ fontSize: "1.2rem", textAlign: "left" }}>
                          Price: ${plan.networking.unit_price}
                        </div>
                      </>
                    ) : (
                      <div style={{ textAlign: "left" }}>
                        <span style={{ fontSize: "1.1rem" }}>Networking: Not Available</span>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <Typography align="center">No data available</Typography>
              )}
            </CardContent>
            {plan && (
              <CardContent>
                <div style={{ fontSize: "1.2rem", textAlign: "center" }}>
                  <strong>Monthly Total: </strong> 
                  <span style={{
                    color: plan.budget === "yes" ? "green" : plan.budget === "no" ? "red" : "black",
                    fontSize: "1.2rem"
                  }}>
                     ${plan.monthly || "-"}
                  </span> 
                  <br />
                  <strong>Annual Total: </strong>
                  <span style={{
                    color: plan.budget === "yes" ? "green" : plan.budget === "no" ? "red" : "black",
                    fontSize: "1.2rem"
                  }}>
                     ${plan.annual || "-"}
                  </span>
                </div>
              </CardContent>
            )}
          </Card>
        );
      })}
      {/* Add additional placeholder cards if plans array is empty */}
      {!Array.isArray(plans) ||
        (plans.length === 0 && (
          <Card sx={{ maxWidth: 345, m: 2, display: "flex", flexDirection: "column" }}>
            <CardContent>
              <Typography align="center">No data available</Typography>
            </CardContent>
          </Card>
        ))}
    </Box>
  </Box>
  );
};

export default RecommendedPlans