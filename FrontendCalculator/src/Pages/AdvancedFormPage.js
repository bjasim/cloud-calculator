import Navbar from "../Components/Navbar";
import Footer from "../Components/Footer";
import AdvancedForm from "../Forms/AdvancedForm";

const AdvancedFormPage = () => {
  return (
    <div>
      <Navbar />
      <AdvancedForm />
      <Footer style={{ marginTop: "150px" }} />
    </div>
  );
};

export default AdvancedFormPage;
