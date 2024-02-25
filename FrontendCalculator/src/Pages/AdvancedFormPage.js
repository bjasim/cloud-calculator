import Navbar from "../Components/Navbar";
import Footer from "../Components/Footer";
import AdvancedForm from "../Forms/AdvancedForm";
import ShowResults from "../Forms/ShowResults";

const AdvancedFormPage = () => {
  return (
    <div>
      <Navbar />
      <AdvancedForm />
      <ShowResults />
      <Footer style={{ marginTop: "150px" }} />
    </div>
  );
};

export default AdvancedFormPage;
