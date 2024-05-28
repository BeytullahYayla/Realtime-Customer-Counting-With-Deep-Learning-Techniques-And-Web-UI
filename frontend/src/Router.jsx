import { useState, useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import LastMonthStats from "./pages/LastMonthStats";
import LastThreeMonthStats from "./pages/LastThreeMonthStats";
import Records from "./pages/Records";
import { Routes, Route, useLocation } from "react-router-dom";
import { useData, getData, useStores, getStores, getUserRole } from "./data/Fetch";
import Loading from "./components/Loading";
import UserManagement from "./pages/UserManagement";
import Account from "./pages/Account";

function Router() {
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
  const role = getUserRole()

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
    setLoadingByDateRange(true);
  }, [location]);
  
  while (!data.length) {
    return <Loading/>;
  }

  const OpenSidebar = () => {
    setOpenSidebarToggle(!openSidebarToggle);
  };

  return (
    <div className="grid-container">
      <Header OpenSidebar={OpenSidebar} setLoading={setLoading} setLoadingByDateRange={setLoadingByDateRange} setStoreName={setStoreName}/>
      <Sidebar openSidebarToggle={openSidebarToggle} OpenSidebar={OpenSidebar} />
      <Routes>
        <Route path="/" element={<Home storeName={storeName} setLoadingByDateRange={setLoadingByDateRange} />} />
        <Route path="/LastMonthStats"  element={<LastMonthStats storeName={storeName} setLoadingByDateRange={setLoadingByDateRange}/>} />
        <Route path="/LastThreeMonthStats"  element={<LastThreeMonthStats storeName={storeName} setLoadingByDateRange={setLoadingByDateRange} />} />
        <Route path="/Records" element={<Records />} />
        <Route path="/Account" element={<Account />} />
        {
          role === "superuser" ? 
          (<Route path="/UserManagement" element={<UserManagement />} />) : ""
        }
      </Routes>
    </div>
  );
}

export default Router;
