import React from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom
import AboutBackground from "../Assets/about-background.png";
import AboutBackgroundImage from "../Assets/about-background-image.png";

const About = () => {
  return (
    <div className="about-section-container">
      <div className="about-background-image-container">
        <img src={AboutBackground} alt="" />
      </div>
      <div className="about-section-image-container">
        <img src={AboutBackgroundImage} alt="" />
      </div>
      <div className="about-section-text-container">
        <h1 className="primary-heading">What's so great about BudgetCloud?</h1>
        <p className="primary-text">
          BudgetCloud is a dynamic company that specializes in providing cloud computing price
          estimates. It operates by taking user-provided data, such as computing needs, storage
          requirements, and desired cloud services, and then generates price quotes across different
          cloud providers.
        </p>
        <p className="primary-text">Click below to learn more</p>
        <div className="about-buttons-container">
          {/* Use Link component with 'to' attribute set to '/learnmore' */}
          <Link to="/contact" style={{ textDecoration: "none" }}>
            {" "}
            {/* Style textDecoration to "none" */}
            <button className="secondary-button">Learn More</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default About;
