import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import ChooseFormsPage from "./Pages/ChooseFormsPage";
import AboutPage from "./Pages/AboutPage";
import TestimonialsPage from "./Pages/TestimonialsPage";
import ContactPage from "./Pages/ContactPage";
import HomePage from "./Pages/HomePage";
import LearnMorePage from "./Pages/LearnMorePage";
import AdvancedFormPage from "./Pages/AdvancedFormPage";
import BasicFormPage from "./Pages/BasicFormPage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="" element={<HomePage />} />
          <Route path="/About" element={<AboutPage />} />
          <Route path="/form" element={<ChooseFormsPage />} />
          <Route path="/form/advancedform" element={<AdvancedFormPage />} />
          <Route path="/form/basicform" element={<BasicFormPage />} />
          <Route path="/testimonials" element={<TestimonialsPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/learnmore" element={<LearnMorePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
