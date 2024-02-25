import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import Navbar from "../Components/Navbar";
import BannerImage from "../Assets/home-banner-image.png";
import { FiArrowRight } from "react-icons/fi";

const Home = () => {
  const navigate = useNavigate(); // Use the useNavigate hook

  // Function to handle button click
  const handleCalculateClick = () => {
    navigate("/form"); // Navigate to the calculate page
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <Navbar />
      <div className="home-banner-container" style={{ flex: 1 }}>
        <div className="home-bannerImage-container"></div>
        <div className="home-text-section">
          <h1 className="primary-heading">Cloud Pricing</h1>
          <p className="primary-text">
            Welcome to BudgetCloud!
            <br />
            Click below to begin filling out a form.
          </p>
          <button className="secondary-button" onClick={handleCalculateClick}>
            Calculate
            <FiArrowRight />
          </button>
        </div>
        <div className="home-image-container">
          <img src={BannerImage} alt="" />
        </div>
      </div>
    </div>
  );
};

export default Home;
