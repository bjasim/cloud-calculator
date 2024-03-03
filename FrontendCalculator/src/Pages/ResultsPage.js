import Navbar from "../Components/Navbar";
import ShowResults from "../Forms/ShowResults";
import Footer from "../Components/Footer";
import { useLocation } from "react-router-dom";

const ResultsPage = () => {
  const { state } = useLocation();
  return (
    <div>
      <Navbar />
      <ShowResults responseData={state && state.responseData} />
      <Footer />
    </div>
  );
};

export default ResultsPage;
