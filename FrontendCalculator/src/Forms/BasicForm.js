import React, { useState, useEffect } from "react";
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

  const [formData, setFormData] = useState({
    computeComplexity: "",
    networkReliability: "",
    dataStorageSize: "",
    databaseService: "",
    monthlyBudget: "",
    resourceGrowth: "",
  });

  const [validationErrors, setValidationErrors] = useState({
    computeComplexity: false,
    networkReliability: false,
    dataStorageSize: false,
    databaseService: false,
    monthlyBudget: false,
    resourceGrowth: false,
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
      try {
        const response = await fetch("http://localhost:8000/api/submit-basic-form/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });
        if (response.ok) {
          // Handle success
          console.log("Form data submitted successfully");
          // Redirect to /results URL upon successful form submission
          navigate("/results"); // Redirect to /results on successful form submission
        } else {
          // Handle error
          console.error("Failed to submit form data");
        }
      } catch (error) {
        console.error("Error submitting form data:", error);
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
                  <MenuItem value="simple">
                    Simple: Basic computing tasks with minimal processing requirements
                  </MenuItem>
                  <MenuItem value="moderate">
                    Moderate: Moderate computing tasks with occasional spikes in processing needs
                  </MenuItem>
                  <MenuItem value="complex">
                    Complex: Intensive computing tasks with high processing demands and complex
                    algorithms
                  </MenuItem>
                </Select>
                {validationErrors.computeComplexity && (
                  <FormHelperText error>Please select compute complexity</FormHelperText>
                )}
              </FormControl>
            </Grid>

            {/* Network Reliability */}
            <Grid item xs={10}>
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
            <Grid item xs={10}>
              <FormControl fullWidth variant="outlined">
                <InputLabel id="data-storage-size-label">Data Storage Size</InputLabel>
                <Select
                  labelId="data-storage-size-label"
                  id="data-storage-size-select"
                  value={formData.dataStorageSize}
                  onChange={handleChange}
                  label="Data Storage Size"
                  name="dataStorageSize"
                  error={validationErrors.dataStorageSize}
                >
                  <MenuItem value="">Select...</MenuItem>
                  <MenuItem value="small">Small: Up to 100GB of data storage</MenuItem>
                  <MenuItem value="medium">Medium: 100GB to 1TB of data storage</MenuItem>
                  <MenuItem value="large">Large: More than 1TB of data storage</MenuItem>
                  <MenuItem value="verylarge">Very Large: More than 100 TB of data</MenuItem>
                </Select>
                {validationErrors.dataStorageSize && (
                  <FormHelperText error>Please select data storage size</FormHelperText>
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
                  <MenuItem value="sql">
                    SQL: Relational database for structured data storage and querying
                  </MenuItem>
                  <MenuItem value="nosql">
                    NoSQL: Non-relational database for flexible data models
                  </MenuItem>
                  <MenuItem value="nodatabase">
                    No database required: No need for a database service at the moment
                  </MenuItem>
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

            {/* Resource Growth */}
            <Grid item xs={10}>
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
            </Grid>

            {/* Submit Button */}
            <Grid item xs={10}>
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

export default BasicForm;
