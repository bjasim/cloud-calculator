import Navbar from "../Components/Navbar";
import Footer from "../Components/Footer";
import BasicForm from "../Forms/BasicForm";

const BasicFormPage = () => {
  return (
    <div>
      <Navbar />
      <BasicForm />
      <Footer style={{ marginTop: "150px" }} />
    </div>
  );
};

export default BasicFormPage;
