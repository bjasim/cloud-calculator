import React from "react";
import Footer from "../Components/Footer";
import Home from "../Components/Home";
import About from "../Components/About";

const HomePage = () => {
  return (
    <div>
      <Home />
      <About />
      <Footer style={{ marginTop: "250px" }} />
    </div>
  );
};

export default HomePage;
