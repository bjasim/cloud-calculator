import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import CircularProgress from "@mui/material/CircularProgress";
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

const AdvancedForm = () => {
  const navigate = useNavigate(); // Initialize navigate function
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    // businessSize: "",
    // expectedUsers: "",
    monthlyBudget: "",
    expectedRAM: "",
    databaseService: "",
    databaseSize: "",
    cloudStorage: "",
    storageSize: "",
    // networkPerformance: "",
    dnsConnection: "",
    cdnConnection: "",
    scalability: "",
    location: "",
  });

  const [validationErrors, setValidationErrors] = useState({
    // businessSize: false,
    // expectedUsers: false,
    monthlyBudget: false,
    expectedRAM: false,
    databaseService: false,
    databaseSize: false,
    cloudStorage: false,
    storageSize: false,
    // networkPerformance: false,
    dnsConnection: false,
    cdnConnection: false,
    scalability: false,
    location: false,
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
        const response = await fetch("http://localhost:8000/api/submit-advanced-form/", {
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

          setTimeout(() => {
            setLoading(false); // Stop loading after delay
            navigate("/results", { state: { responseData } });
          }, 3000); // Delay 5 seconds before navigating
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

  return (
    <Container maxWidth="md">
      <Box mt={5} mb={5}>
        <Typography variant="h4" align="center" mb={4}>
          Advanced Analysis Form
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={4}>
            {/* Business Size */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="monthly-budget-label">Monthly Budget</InputLabel>
                <Select
                  labelId="monthly-budget-label"
                  value={formData.monthlyBudget}
                  onChange={handleChange}
                  name="monthlyBudget"
                  label="Monthly Budget"
                  error={validationErrors.monthlyBudget}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="lessThan500">Less than $500</MenuItem>
                  <MenuItem value="500to2000">$500 to $2000</MenuItem>
                  <MenuItem value="2000to5000">$2000 to $5000</MenuItem>
                  <MenuItem value="moreThan5000">More than $5000</MenuItem>
                </Select>
                {validationErrors.monthlyBudget && (
                  <FormHelperText error>Please select monthly budget</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* Expected CPU&RAM */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="expected-cpu-ram">Expected vCPU and RAM</InputLabel>
                <Select
                  labelId="expected-cpu-ram"
                  value={formData.expectedRAM}
                  onChange={handleChange}
                  name="expectedRAM"
                  label="Expected Users"
                  error={validationErrors.expectedRAM}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="1vCPU">1 vCPU - 2 RAM</MenuItem>
                  <MenuItem value="2vCPUs">2 vCPU - 4 RAM</MenuItem>
                  <MenuItem value="4vCPUs">4 vCPU - 16 RAM</MenuItem>
                  <MenuItem value="8vCPUs">8 vCPU - 32 RAM</MenuItem>
                  <MenuItem value="12vCPUs">12 vCPU - 48 RAM</MenuItem>
                  <MenuItem value="16vCPUs">16 vCPU - 64 RAM</MenuItem>
                </Select>
                {validationErrors.expectedRAM && (
                  <FormHelperText error>Please select expected users</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Database Services */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="database-service-label">Database Services</InputLabel>
                <Select
                  labelId="database-service-label"
                  value={formData.databaseService}
                  onChange={handleChange}
                  name="databaseService"
                  label="Database Services"
                  error={validationErrors.databaseService}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="noSQL">NoSQL</MenuItem>
                  <MenuItem value="sql">SQL</MenuItem>
                  <MenuItem value="noDatabase">No Database Required</MenuItem>
                </Select>
                {validationErrors.databaseService && (
                  <FormHelperText error>Please select database service</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Database Size */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="database-size-label">Database Size</InputLabel>
                <Select
                  labelId="database-size-label"
                  value={formData.databaseSize}
                  onChange={handleChange}
                  name="databaseSize"
                  label="Database Size"
                  error={validationErrors.databaseSize}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="small">10GB</MenuItem>
                  <MenuItem value="medium">100GB</MenuItem>
                  <MenuItem value="large">1TB</MenuItem>
                  <MenuItem value="noDatabase">Not database required</MenuItem>
                </Select>
                {validationErrors.databaseSize && (
                  <FormHelperText error>Please select database size</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Cloud Storage */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="cloud-storage-label">Cloud Storage</InputLabel>
                <Select
                  labelId="cloud-storage-label"
                  value={formData.cloudStorage}
                  onChange={handleChange}
                  name="cloudStorage"
                  label="Cloud Storage"
                  error={validationErrors.cloudStorage}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="Object Storage">Object Storage</MenuItem>
                  <MenuItem value="File Storage">File Storage (EFS)</MenuItem>
                  <MenuItem value="Block Storage">Block Storage (EBS)</MenuItem>
                  <MenuItem value="No Storage">No Storage Required</MenuItem>
                </Select>
                {validationErrors.cloudStorage && (
                  <FormHelperText error>Please select cloud storage</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Storage Size */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="storage-size-label">Storage Size</InputLabel>
                <Select
                  labelId="storage-size-label"
                  value={formData.storageSize}
                  onChange={handleChange}
                  name="storageSize"
                  label="Storage Size"
                  error={validationErrors.storageSize}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="small">1TB</MenuItem>
                  <MenuItem value="medium">10TB</MenuItem>
                  <MenuItem value="large">100TB</MenuItem>
                  <MenuItem value="notSure">No storage required</MenuItem>
                </Select>
                {validationErrors.storageSize && (
                  <FormHelperText error>Please select storage size</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Network Performance */}
            {/* <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="network-performance-label">Network Performance</InputLabel>
                <Select
                  labelId="network-performance-label"
                  value={formData.networkPerformance}
                  onChange={handleChange}
                  name="networkPerformance"
                  label="Network Performance"
                  error={validationErrors.networkPerformance}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="basic">Basic</MenuItem>
                  <MenuItem value="standard">Standard</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="veryHigh">Very High</MenuItem>
                </Select>
                {validationErrors.networkPerformance && (
                  <FormHelperText error>Please select network performance</FormHelperText>
                )}
              </FormControl>
            </Grid> */}

            {/* Content Delivery Network (CDN) */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="dns-feature-laber">Domain Name System (DNS)</InputLabel>
                <Select
                  labelId="dns-feature-laber"
                  value={formData.dnsConnection}
                  onChange={handleChange}
                  name="dnsConnection"
                  label="dns connection"
                  error={validationErrors.dnsConnection}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
                {validationErrors.dnsConnection && (
                  <FormHelperText error>Please select your option</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Content Delivery Network (CDN) */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="cdn-feature-laber">Content Delivery Network (CDN)</InputLabel>
                <Select
                  labelId="cdn-feature-laber"
                  value={formData.cdnConnection}
                  onChange={handleChange}
                  name="cdnConnection"
                  label="cdn connection"
                  error={validationErrors.cdnConnection}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
                {validationErrors.cdnConnection && (
                  <FormHelperText error>Please select your option</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Scalability */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="scalability-label">Scalability</InputLabel>
                <Select
                  labelId="scalability-label"
                  value={formData.scalability}
                  onChange={handleChange}
                  name="scalability"
                  label="Scalability"
                  error={validationErrors.scalability}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="notImportant">Not Important</MenuItem>
                  {/* <MenuItem value="somewhatImportant">Somewhat Important</MenuItem> */}
                  {/* <MenuItem value="veryImportant">Very Important</MenuItem> */}
                  <MenuItem value="essential">Essential</MenuItem>
                </Select>
                {validationErrors.scalability && (
                  <FormHelperText error>Please select scalability</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* Location */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="location-label">Location</InputLabel>
                <Select
                  labelId="location-label"
                  value={formData.location}
                  onChange={handleChange}
                  name="location"
                  label="Location"
                  error={validationErrors.location}
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
                {validationErrors.location && (
                  <FormHelperText error>Please select a location</FormHelperText>
                )}
              </FormControl>
            </Grid>
            {/* Submit Button */}
            <Grid item xs={12}>
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

export default AdvancedForm;
