import React, { useState, useEffect} from "react";
import CircularProgress from "@mui/material/CircularProgress";
import { useNavigate } from "react-router-dom"; // Import useNavigate
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
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
    // Clear databaseSize error if 'noDatabase' is selected
    if (name === "databaseService" && value === "noDatabase") {
      setValidationErrors(prevErrors => ({
        ...prevErrors,
        [name]: value === "",
        databaseSize: false, // Do not validate databaseSize if 'noDatabase' is selected
      }));
    } else {
      setValidationErrors(prevErrors => ({
        ...prevErrors,
        [name]: value === "",
      }));
    }
  };
  
  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   let isValid = true;
  //   const newValidationErrors = { ...validationErrors };
  //   Object.entries(formData).forEach(([key, value]) => {
  //     // Skip validation for databaseSize if 'noDatabase' is selected
  //     if ((key === "databaseSize" && formData.databaseService === "noDatabase") || 
  //         (key === "storageSize" && formData.cloudStorage === "No Storage")) {
  //       newValidationErrors[key] = false;
  //     } else if (value === "") {
  //       isValid = false;
  //       newValidationErrors[key] = true;
  //     } else {
  //       newValidationErrors[key] = false;
  //     }
  //   });
  
  //   // Update state immediately, no need to delay with setTimeout
  //   setValidationErrors(newValidationErrors);
  
  //   if (isValid) {
  //     setLoading(true);
  //     try {
  //       const response = await fetch("http://localhost:8000/api/submit-advanced-form/", {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify(formData),
  //       });
  //       if (response.ok) {
  //         console.log("Form data submitted successfully");
  //         const responseData = await response.json(); 
  //         navigate("/results", { state: { responseData } });
  //         console.log("Response from backend:", responseData);

  //         // Delay 5 seconds before navigating to the results page
  //         setTimeout(() => {
  //           setLoading(false); // Stop loading after the response
  //           navigate("/results", { state: { responseData } });
  //         }, 3000);
  //       } else {
  //         console.error("Failed to submit form data");
  //         setLoading(false);
  //       }
  //     } catch (error) {
  //       console.error("Error submitting form data:", error);
  //       setLoading(false);
  //     }
  //   }
  // };
  const handleSubmit = async (event) => {
    event.preventDefault();
    let isValid = true;
    const newValidationErrors = { ...validationErrors };
    Object.entries(formData).forEach(([key, value]) => {
      if ((key === "databaseSize" && formData.databaseService === "noDatabase") || 
          (key === "storageSize" && formData.cloudStorage === "No Storage")) {
        newValidationErrors[key] = false;
      } else if (value === "") {
        isValid = false;
        newValidationErrors[key] = true;
      } else {
        newValidationErrors[key] = false;
      }
    });
  
    setValidationErrors(newValidationErrors);
  
    if (isValid) {
      setLoading(true); // Ensure loading is set to true before starting the fetch
      try {
        const response = await fetch("http://localhost:8000/api/submit-advanced-form/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });
        if (response.ok) {
          const responseData = await response.json();
          // Introduce a delay here using setTimeout
          setTimeout(() => {
            setLoading(false); // Stop loading and then navigate
            navigate("/results", { state: { responseData } });
          }, 3000); // Adjust the delay as needed
        } else {
          console.error("Failed to submit form data");
          setLoading(false); // Ensure loading is set to false on failure
        }
      } catch (error) {
        console.error("Error submitting form data:", error);
        setLoading(false); // Ensure loading is set to false on exception
      }
    }
  };
  
  

  // Determine if Database Size and Storage Size should be disabled
  const isDatabaseDisabled = !formData.databaseService || formData.databaseService === "noDatabase";
  const isStorageDisabled = !formData.cloudStorage || formData.cloudStorage === "No Storage";  

  useEffect(() => {
    const timer = setTimeout(() => {
      setValidationErrors({
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
    }, 3000);
    return () => clearTimeout(timer);
  }, [validationErrors]);

  return (
    <Container maxWidth="md">
      <Box mt={5} mb={5}>
        <Typography variant="h4" align="center" mb={4}>
          Advanced Analysis Form
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={4}>
            {/* Business Size */}
            {/* <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="business-size-label">Business Size</InputLabel>
                <Select
                  labelId="business-size-label"
                  value={formData.businessSize}
                  onChange={handleChange}
                  name="businessSize"
                  label="Business Size"
                  error={validationErrors.businessSize}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="smallBusiness">Small Business / Startup</MenuItem>
                  <MenuItem value="mediumBusiness">Medium-Sized Business</MenuItem>
                  <MenuItem value="largeEnterprise">Large Enterprise</MenuItem>
                  <MenuItem value="creativeAgencies">Creative and Digital Agencies</MenuItem>
                  <MenuItem value="healthEducationNonProfit">
                    Healthcare, Education, and Non-Profit Organizations
                  </MenuItem>
                </Select>
                {validationErrors.businessSize && (
                  <FormHelperText error>Please select business size</FormHelperText>
                )}
              </FormControl>
            </Grid> */}
            {/* Expected Users
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="user-count-label">Expected users</InputLabel>
                <Select
                  labelId="user-count-label"
                  value={formData.expectedUsers}
                  onChange={handleChange}
                  name="expectedUsers"
                  label="How many concurrent users?"
                  error={validationErrors.expectedUsers}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="100-500">100-500 users</MenuItem>
                  <MenuItem value="500-1000">500-1000 users</MenuItem>
                  <MenuItem value="1000-5000">1000-5000 users</MenuItem>
                  <MenuItem value="5000-10000">5000-10000 users</MenuItem>
                  <MenuItem value="moreThan10000">More than 10000 users</MenuItem>
                </Select>
                {validationErrors.expectedUsers && (
                  <FormHelperText error>Please select expected users</FormHelperText>
                )}
              </FormControl>
            </Grid> */}
            {/* Monthly Budget */}
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
            {/* <Grid item xs={6}>
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
                  <MenuItem value="small">Small (under 1 TB)</MenuItem>
                  <MenuItem value="medium">Medium (1-10 TB)</MenuItem>
                  <MenuItem value="large">Large (10-100 TB)</MenuItem>
                  <MenuItem value="veryLarge">Very Large (over 100 TB)</MenuItem>
                  <MenuItem value="notSure">Not Sure/No Specific Requirements</MenuItem>
                </Select>
                {validationErrors.databaseSize && (
                  <FormHelperText error>Please select database size</FormHelperText>
                )}
              </FormControl>
            </Grid> */}

            <Grid item xs={6}>
              <FormControl fullWidth disabled={isDatabaseDisabled}>
                <InputLabel id="database-size-label">Database Size</InputLabel>
                <Select
                  labelId="database-size-label"
                  value={formData.databaseSize}
                  onChange={handleChange}
                  name="databaseSize"
                  label="Database Size"
                  error={validationErrors.databaseSize}
                  disabled={isDatabaseDisabled} // Disable based on condition
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="small">Small (under 1 TB)</MenuItem>
                  <MenuItem value="medium">Medium (10 TB)</MenuItem>
                  <MenuItem value="large">Large (100 TB)</MenuItem>
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
            {/* <Grid item xs={6}>
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
                  <MenuItem value="small">Small (under 1 TB)</MenuItem>
                  <MenuItem value="medium">Medium (1-10 TB)</MenuItem>
                  <MenuItem value="large">Large (10-100 TB)</MenuItem>
                  <MenuItem value="veryLarge">Very Large (over 100 TB)</MenuItem>
                  <MenuItem value="notSure">Not Sure/No Specific Requirements</MenuItem>
                </Select>
                {validationErrors.storageSize && (
                  <FormHelperText error>Please select storage size</FormHelperText>
                )}
              </FormControl>
            </Grid> */}

            <Grid item xs={6}>
              <FormControl fullWidth disabled={isStorageDisabled}>
                <InputLabel id="storage-size-label">Storage Size</InputLabel>
                <Select
                  labelId="storage-size-label"
                  value={formData.storageSize}
                  onChange={handleChange}
                  name="storageSize"
                  label="Storage Size"
                  error={validationErrors.storageSize}
                  disabled={isStorageDisabled} // Disable based on condition
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="small">Small (under 1 TB)</MenuItem>
                  <MenuItem value="medium">Medium (1-10 TB)</MenuItem>
                  <MenuItem value="large">Large (10-100 TB)</MenuItem>
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
