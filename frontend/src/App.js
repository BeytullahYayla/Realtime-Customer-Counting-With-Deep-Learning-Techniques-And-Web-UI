import { useState, useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import LastMonthStats from "./pages/LastMonthStats";
import LastThreeMonthStats from "./pages/LastThreeMonthStats";
import Records from "./pages/Records";
import Settings from "./pages/Settings";
import { Routes, Route, useLocation } from "react-router-dom";
import axios from "axios";
import { useData, getData, useStores, getStores } from "./data/Fetch";

function App() {
  const [openSidebarToggle, setOpenSidebarToggle] = useState(false);
  const { fetchData } = useData();
  const {fetchStores} = useStores();
  const data = getData();
  const stores = getStores();
  const [storeName, setStoreName] = useState(null);
  const [loading, setLoading] = useState(true)
  const [loadingByDateRange, setLoadingByDateRange] = useState(true)
  const [loadingStores, setLoadingStores] = useState(true)
  const location = useLocation();

  useEffect(() => {
    const fetchStoresAsync = async () => {
      try {
        await fetchStores();
        setLoadingStores(false);
      } catch (error) {
        console.error("Veri çekme hatası:", error);
        setLoadingStores(false);
      }
    };

    fetchStoresAsync();
  },[fetchStores])

  useEffect(() => {
    if (stores.length > 0 && !storeName) {
      setStoreName(stores[0].Name);
    }
  }, [stores]);

  useEffect(() => {
    if (storeName) {
      const fetchDataAsync = async () => {
        try {
          await fetchData(storeName);
          setLoading(false);
        } catch (error) {
          console.error("Veri çekme hatası:", error);
          setLoading(false);
        }
      };

      fetchDataAsync();
    }
  }, [fetchData, storeName]);

  useEffect(() => {
    setLoadingByDateRange(true); // Her sayfa değiştiğinde setLoadingByDateRange(true) yap
  }, [location]);
  
  while (!data.length) {
    return <div>Loading...</div>;
  }

  const OpenSidebar = () => {
    setOpenSidebarToggle(!openSidebarToggle);
  };

  return (
    <div className="grid-container">
      <Header OpenSidebar={OpenSidebar} setLoading={setLoading} setLoadingByDateRange={setLoadingByDateRange} setStoreName={setStoreName} />
      <Sidebar
        openSidebarToggle={openSidebarToggle}
        OpenSidebar={OpenSidebar}
      />
      <Routes>
        <Route path="/" element={<Home storeName={storeName} setLoadingByDateRange={setLoadingByDateRange} />} />
        <Route path="/LastMonthStats"  element={<LastMonthStats storeName={storeName} setLoadingByDateRange={setLoadingByDateRange}/>} />
        <Route path="/LastThreeMonthStats"  element={<LastThreeMonthStats storeName={storeName} setLoadingByDateRange={setLoadingByDateRange} />} />
        <Route path="/Records" element={<Records />} />
        <Route path="/Settings" element={<Settings />} />
      </Routes>
    </div>
  );
}

export default App;
