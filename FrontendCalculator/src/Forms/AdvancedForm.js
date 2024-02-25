import React, { useState } from "react";
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
  const [formData, setFormData] = useState({
    businessSize: "",
    expectedUsers: "",
    databaseService: "",
    databaseSize: "",
    cloudStorage: "",
    storageType: "",
    networkPerformance: "",
    networkingFeature: "",
    securityCompliance: "",
    scalability: "",
    monthlyBudget: "",
  });

  const [validationErrors, setValidationErrors] = useState({
    businessSize: false,
    expectedUsers: false,
    databaseService: false,
    databaseSize: false,
    cloudStorage: false,
    storageType: false,
    networkPerformance: false,
    networkingFeature: false,
    securityCompliance: false,
    scalability: false,
    monthlyBudget: false,
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

  const handleSubmit = (event) => {
    event.preventDefault();
    let isValid = true;
    const newValidationErrors = { ...validationErrors };
    Object.entries(formData).forEach(([key, value]) => {
      if (value === "") {
        isValid = false;
        newValidationErrors[key] = true;
        setTimeout(() => {
          setValidationErrors((prevErrors) => ({
            ...prevErrors,
            [key]: false,
          }));
        }, 3000); // Clear error after 3 seconds
      } else {
        newValidationErrors[key] = false;
      }
    });
    setValidationErrors(newValidationErrors);
    if (isValid) {
      console.log("Form Data:", formData);
      // Here, you can send formData to your backend (Django API) using fetch or axios
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
            </Grid>
            {/* Expected Users */}
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
            </Grid>
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
                <InputLabel id="expected-users-label">Expected vCPU and RAM</InputLabel>
                <Select
                  labelId="expected-users-label"
                  value={formData.expectedUsers}
                  onChange={handleChange}
                  name="expectedUsers"
                  label="Expected Users"
                  error={validationErrors.expectedUsers}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="1vCPU">1 vCPU - 2 RAM</MenuItem>
                  <MenuItem value="2vCPU">2 vCPU - 4 RAM</MenuItem>
                  <MenuItem value="4vCPU">4 vCPU - 16 RAM</MenuItem>
                  <MenuItem value="8vCPU">8 vCPU - 32 RAM</MenuItem>
                  <MenuItem value="12vCPU">12 vCPU - 48 RAM</MenuItem>
                  <MenuItem value="16vCPU">16 vCPU - 64 RAM</MenuItem>
                  <MenuItem value="24vCPU">24 vCPU - 96 RAM</MenuItem>
                  <MenuItem value="32vCPU">32 vCPU - 128 RAM</MenuItem>
                  <MenuItem value="48vCPU">48 vCPU - 192 RAM</MenuItem>
                  <MenuItem value="64vCPU">64 vCPU - 256 RAM</MenuItem>
                </Select>
                {validationErrors.expectedUsers && (
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
                  <MenuItem value="postgreSQL">PostgreSQL</MenuItem>
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
                  <MenuItem value="objectStorage">Object Storage</MenuItem>
                  <MenuItem value="fileStorage">File Storage (EFS)</MenuItem>
                  <MenuItem value="blockStorage">Block Storage (EBS)</MenuItem>
                  <MenuItem value="noStorage">No Storage Required</MenuItem>
                </Select>
                {validationErrors.cloudStorage && (
                  <FormHelperText error>Please select cloud storage</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Storage Type */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="storage-type-label">Storage Type</InputLabel>
                <Select
                  labelId="storage-type-label"
                  value={formData.storageType}
                  onChange={handleChange}
                  name="storageType"
                  label="Storage Type"
                  error={validationErrors.storageType}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="highVolume">High Volume Storage</MenuItem>
                  <MenuItem value="fastAccess">Fast Access Storage</MenuItem>
                  <MenuItem value="backupRecovery">Regular Backup and Recovery</MenuItem>
                  <MenuItem value="archivingCompliance">Archiving and Compliance</MenuItem>
                  <MenuItem value="noSpecific">No Specific Requirements</MenuItem>
                  <MenuItem value="noStorage">No Storage Required</MenuItem>
                </Select>
                {validationErrors.storageType && (
                  <FormHelperText error>Please select storage type</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Network Performance */}
            <Grid item xs={6}>
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
            </Grid>

            {/* Networking Features */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="networking-features-label">Networking Features</InputLabel>
                <Select
                  labelId="networking-features-label"
                  value={formData.networkingFeature}
                  onChange={handleChange}
                  name="networkingFeature"
                  label="Networking Features"
                  error={validationErrors.networkingFeature}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="loadBalancing">Load Balancing</MenuItem>
                  <MenuItem value="vpnConnections">VPN Connections</MenuItem>
                  <MenuItem value="contentDeliveryNetwork">Content Delivery Network (CDN)</MenuItem>
                  <MenuItem value="directConnectionToOnPremises">
                    Direct Connection to On-premises
                  </MenuItem>
                </Select>
                {validationErrors.networkingFeature && (
                  <FormHelperText error>Please select networking feature</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Security and Compliance */}
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="security-compliance-label">Security and Compliance</InputLabel>
                <Select
                  labelId="security-compliance-label"
                  value={formData.securityCompliance}
                  onChange={handleChange}
                  name="securityCompliance"
                  label="Security and Compliance"
                  error={validationErrors.securityCompliance}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="standard">Standard</MenuItem>
                  <MenuItem value="enhanced">Enhanced</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="custom">Custom</MenuItem>
                </Select>
                {validationErrors.securityCompliance && (
                  <FormHelperText error>Please select security and compliance</FormHelperText>
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
                  <MenuItem value="somewhatImportant">Somewhat Important</MenuItem>
                  <MenuItem value="veryImportant">Very Important</MenuItem>
                  <MenuItem value="essential">Essential</MenuItem>
                </Select>
                {validationErrors.scalability && (
                  <FormHelperText error>Please select scalability</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Submit Button */}
            <Grid item xs={12}>
              <Box mt={3} textAlign="center">
                <Button variant="contained" color="primary" type="submit">
                  Calculate
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Box>
    </Container>
  );
};

export default AdvancedForm;
