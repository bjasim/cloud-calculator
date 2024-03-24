import React, { useState, useEffect } from "react";
import CircularProgress from "@mui/material/CircularProgress";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Container,
  Grid,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  FormHelperText,
} from "@mui/material";

const BasicForm = () => {
  const navigate = useNavigate(); // Initialize navigate function
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    computeComplexity: "",
    expectedUsers: "",
    dataStorageType: "",
    databaseService: "",
    monthlyBudget: "",
    dnsFeature: "",
    cdnNetworking: "",
    region: "",
    // networkReliability: "",
    // dataStorageSize: "",
    // resourceGrowth: "",
  });

  const [validationErrors, setValidationErrors] = useState({
    computeComplexity: false,
    expectedUsers: false,
    dataStorageType: false,
    databaseService: false,
    monthlyBudget: false,
    dnsFeature: false,
    cdnNetworking: false,
    region: false,
    // networkReliability: false,
    // dataStorageSize: false,
    // resourceGrowth: false,
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    setValidationErrors((prevErrors) => ({
      ...prevErrors,
      [name]: value === "",
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    let isValid = true;
    const newValidationErrors = { ...validationErrors };
    Object.entries(formData).forEach(([key, value]) => {
      if (value === "") {
        isValid = false;
        newValidationErrors[key] = true;
      } else {
        newValidationErrors[key] = false;
      }
    });
    setValidationErrors(newValidationErrors);

    if (isValid) {
      setLoading(true); // Start loading before the request
      try {
        const response = await fetch("http://localhost:8000/api/submit-basic-form/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });
        if (response.ok) {
          console.log("Form data submitted successfully");
          // Handle success
          const responseData = await response.json(); // Parse response body as JSON
          console.log("Response from backend:", responseData); // Print the response

          // Delay 5 seconds before navigating to the results page
          setTimeout(() => {
            setLoading(false); // Stop loading after the response
            navigate("/results", { state: { responseData } });
          }, 3000);
        } else {
          // Handle error
          console.error("Failed to submit form data");
          setLoading(false); // Stop loading on error
        }
      } catch (error) {
        console.error("Error submitting form data:", error);
        setLoading(false); // Stop loading on exception
      }
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setValidationErrors({
        computeComplexity: false,
        networkReliability: false,
        dataStorageSize: false,
        databaseService: false,
        monthlyBudget: false,
        resourceGrowth: false,
      });
    }, 3000);
    return () => clearTimeout(timer);
  }, [validationErrors]);

  return (
    <Container maxWidth="md">
      <Box mt={5} mb={5}>
        <Typography variant="h4" align="center" mb={4}>
          Basic Analysis Form
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={4} justifyContent="center">
            {/* Compute Complexity */}
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="compute-complexity-label">Compute Complexity</InputLabel>
                <Select
                  labelId="compute-complexity-label"
                  id="compute-complexity-select"
                  value={formData.computeComplexity}
                  onChange={handleChange}
                  label="Compute Complexity"
                  name="computeComplexity"
                  error={validationErrors.computeComplexity}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="simple">Basic Computing</MenuItem>
                  <MenuItem value="moderate">Moderate</MenuItem>
                  <MenuItem value="complex">Intensive</MenuItem>
                </Select>
                {validationErrors.computeComplexity && (
                  <FormHelperText error>Please select compute complexity</FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="compute-complexity-label">Expected Users</InputLabel>
                <Select
                  labelId="compute-complexity-label"
                  id="compute-complexity-select"
                  value={formData.expectedUsers}
                  onChange={handleChange}
                  label="Compute Complexity"
                  name="expectedUsers"
                  error={validationErrors.expectedUsers}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="1000">Less than 1000</MenuItem>
                  <MenuItem value="5000">5000</MenuItem>
                  <MenuItem value="10000">10000+</MenuItem>
                </Select>
                {validationErrors.expectedUsers && (
                  <FormHelperText error>Please select compute complexity</FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="compute-complexity-label">
                  What type of data do you work with ?
                </InputLabel>
                <Select
                  labelId="compute-complexity-label"
                  id="compute-complexity-select"
                  value={formData.dataStorageType}
                  onChange={handleChange}
                  label="Compute Complexity"
                  name="dataStorageType"
                  error={validationErrors.dataStorageType}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="files">Files</MenuItem>
                  <MenuItem value="databases">Databases</MenuItem>
                  <MenuItem value="multimedia">Multimedia</MenuItem>
                </Select>
                {validationErrors.dataStorageType && (
                  <FormHelperText error>Please select data storage type</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* Database Service */}
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="database-service-label">Database Service</InputLabel>
                <Select
                  labelId="database-service-label"
                  id="database-service-select"
                  value={formData.databaseService}
                  onChange={handleChange}
                  label="Database Service"
                  name="databaseService"
                  error={validationErrors.databaseService}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="basic">Basic Database</MenuItem>
                  <MenuItem value="complex">Complex Database</MenuItem>
                  <MenuItem value="nodatabase">No database</MenuItem>
                </Select>
                {validationErrors.databaseService && (
                  <FormHelperText error>Please select database service</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* Monthly Budget */}
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="monthly-budget-label">Monthly Budget</InputLabel>
                <Select
                  labelId="monthly-budget-label"
                  id="monthly-budget-select"
                  value={formData.monthlyBudget}
                  onChange={handleChange}
                  label="Monthly Budget"
                  name="monthlyBudget"
                  error={validationErrors.monthlyBudget}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="under50">Economy: Less than $500 per month</MenuItem>
                  <MenuItem value="500to2000">Standard: Between $500 and $2000 per month</MenuItem>
                  <MenuItem value="2000to5000">Premium: Between $2000 and $5000 per month</MenuItem>
                  <MenuItem value="over5000">Business: More than $5000 per month</MenuItem>
                </Select>
                {validationErrors.monthlyBudget && (
                  <FormHelperText error>Please select monthly budget</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* DNS Feature */}
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="dns-feature-label">
                  Do you want to ensure that your website is identifiable by a user-friendly
                  address?
                </InputLabel>
                <Select
                  labelId="dns-feature-label"
                  id="dns-feature-select"
                  value={formData.dnsFeature}
                  onChange={handleChange}
                  label="DNS Networking"
                  name="dnsFeature"
                  error={validationErrors.dnsFeature}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
                {validationErrors.dnsFeature && (
                  <FormHelperText error>Please select your option</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* DNS Feature */}
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="cdn-feature-label">
                  Do you have a website with global users and want to minimize delays in loading
                  content?{" "}
                </InputLabel>
                <Select
                  labelId="cdn-feature-label"
                  id="cdn-feature-select"
                  value={formData.cdnNetworking}
                  onChange={handleChange}
                  label="CDN Networking"
                  name="cdnNetworking"
                  error={validationErrors.cdnNetworking}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
                {validationErrors.cdnNetworking && (
                  <FormHelperText error>Please select your option</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* Region */}
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="dns-feature-label">Region</InputLabel>
                <Select
                  labelId="dns-feature-label"
                  id="dns-feature-select"
                  value={formData.region}
                  onChange={handleChange}
                  label="Region"
                  name="region"
                  error={validationErrors.region}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="us-east-1">US East (N. Virginia)</MenuItem>
                  <MenuItem value="us-east-2">US East (Ohio)</MenuItem>
                  <MenuItem value="us-west-1">US West (N. California)</MenuItem>
                  <MenuItem value="us-west-2">US West (Oregon)</MenuItem>
                  <MenuItem value="ap-east-1">Asia Pacific (Hong Kong)</MenuItem>
                  <MenuItem value="ap-south-1">Asia Pacific (Mumbai)</MenuItem>
                  <MenuItem value="ap-northeast-3">Asia Pacific (Osaka-Local)</MenuItem>
                  <MenuItem value="ap-northeast-2">Asia Pacific (Seoul)</MenuItem>
                  <MenuItem value="ap-southeast-1">Asia Pacific (Singapore)</MenuItem>
                  <MenuItem value="ap-southeast-2">Asia Pacific (Sydney)</MenuItem>
                  <MenuItem value="ap-northeast-1">Asia Pacific (Tokyo)</MenuItem>
                  <MenuItem value="ca-central-1">Canada (Central)</MenuItem>
                  <MenuItem value="cn-north-1">China (Beijing)</MenuItem>
                  <MenuItem value="cn-northwest-1">China (Ningxia)</MenuItem>
                  <MenuItem value="eu-central-1">EU (Frankfurt)</MenuItem>
                  <MenuItem value="eu-west-1">EU (Ireland)</MenuItem>
                  <MenuItem value="eu-west-2">EU (London)</MenuItem>
                  <MenuItem value="eu-south-1">EU (Milan)</MenuItem>
                  <MenuItem value="eu-west-3">EU (Paris)</MenuItem>
                  <MenuItem value="eu-north-1">EU (Stockholm)</MenuItem>
                  <MenuItem value="me-south-1">Middle East (Bahrain)</MenuItem>
                  <MenuItem value="sa-east-1">South America (Sao Paulo)</MenuItem>
                  <MenuItem value="af-south-1">Africa (Cape Town)</MenuItem>
                </Select>
                {validationErrors.region && (
                  <FormHelperText error>Please select your region</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Network Reliability */}
            {/* <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="network-reliability-label">Network Reliability</InputLabel>
                <Select
                  labelId="network-reliability-label"
                  id="network-reliability-select"
                  value={formData.networkReliability}
                  onChange={handleChange}
                  label="Network Reliability"
                  name="networkReliability"
                  error={validationErrors.networkReliability}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="low">
                    Basic: Basic network connectivity with minimal downtime
                  </MenuItem>
                  <MenuItem value="medium">
                    Moderate: Reliable network with occasional downtime for maintenance
                  </MenuItem>
                  <MenuItem value="high">
                    High: High availability network with minimal downtime and fast response times
                  </MenuItem>
                </Select>
                {validationErrors.networkReliability && (
                  <FormHelperText error>Please select network reliability</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Data Storage Size */}
            {/* <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="data-storage-type-label">What type of data do you work with ?</InputLabel>
                <Select
                  labelId="data-storage-type-label"
                  id="data-storage-type-select"
                  value={formData.dataStorageType}
                  onChange={handleChange}
                  label="Data Storage Type"
                  name="dataStorageType"
                  error={validationErrors.dataStorageType}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="files">Files</MenuItem>
                  <MenuItem value="databases">Databases</MenuItem>
                  <MenuItem value="multimedia">Multimedia</MenuItem>
                </Select>
                {validationErrors.dataStorageType && (
                  <FormHelperText error>Please select data storage type</FormHelperText>
                )}
              </FormControl>
            </Grid>  */}

            {/* Resource Growth */}
            {/* <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="resource-growth-label">Resource Growth</InputLabel>
                <Select
                  labelId="resource-growth-label"
                  id="resource-growth-select"
                  value={formData.resourceGrowth}
                  onChange={handleChange}
                  label="Resource Growth"
                  name="resourceGrowth"
                  error={validationErrors.resourceGrowth}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="slow">Slow: Gradual resource growth over time</MenuItem>
                  <MenuItem value="moderate">Moderate: Steady resource growth</MenuItem>
                  <MenuItem value="fast">Fast: Rapid resource expansion</MenuItem>
                </Select>
                {validationErrors.resourceGrowth && (
                  <FormHelperText error>Please select resource growth</FormHelperText>
                )}
              </FormControl>
            </Grid> */}

            {/* Submit Button */}
            <Grid item xs={10}>
              <Box mt={3} textAlign="center" position="relative">
                <Button variant="contained" color="primary" type="submit" disabled={loading}>
                  Calculate
                </Button>
                {loading && (
                  <CircularProgress size={24} style={{ position: "absolute", top: "5px" }} />
                )}
              </Box>
            </Grid>
          </Grid>
        </form>
      </Box>
    </Container>
  );
};

export default BasicForm;
