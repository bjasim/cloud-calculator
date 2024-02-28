import Navbar from "../Components/Navbar";
import Footer from "../Components/Footer";
import BasicForm from "../Forms/BasicForm";
import ShowResults from "../Forms/ShowResults";

const BasicFormPage = () => {
  return (
    <div>
      <Navbar />
      <BasicForm />
      <ShowResults />
      <Footer style={{ marginTop: "150px" }} />
    </div>
  );
};

export default BasicFormPage;
