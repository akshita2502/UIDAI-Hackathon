import React, { useState } from "react";
import { Provider } from "react-redux";
import { store } from "./store/store";
import AnomalyTypes from "./components/AnomalyTypes";
import SidePanel from "./components/SidePanel";
import MainPanel from "./components/MainPanel";
import BottomPanel from "./components/BottomPanel";

const App: React.FC = () => {
  const [activePage, setActivePage] = useState("anomaly types");

  const renderContent = () => {
    switch (activePage) {
      case "anomaly types":
        return <AnomalyTypes />;
      case "heatmap":
        return <MainPanel />;
      case "analytics":
        return <BottomPanel />;
      case "statewise":
        return (
          <div style={{ 
            height: "100%", 
            display: "flex", 
            justifyContent: "center", 
            alignItems: "center", 
            color: "var(--text-secondary)",
            flexDirection: "column"
          }}>
            <h2 style={{fontSize: "24px", marginBottom: "8px"}}>🚧 Work in Progress</h2>
            <p>State-wise analytics module is under development.</p>
          </div>
        );
      default:
        return <MainPanel />;
    }
  };

  return (
    <Provider store={store}>
      <div style={{ 
        display: "flex", 
        height: "100vh", 
        width: "100vw", 
        overflow: "hidden",
        backgroundColor: "var(--bg-color)" 
      }}>
        {/* Left SidePanel */}
        <SidePanel activePage={activePage} onNavigate={setActivePage} />

        {/* Main Content Area */}
        <main style={{ 
          flex: 1, 
          display: "flex", 
          flexDirection: "column",
          position: "relative",
          overflow: "hidden" 
        }}>
          {/* Top Header (Simplified, since SidePanel has the logo now) */}
          <header style={{
            height: "60px",
            backgroundColor: "#FFFFFF",
            borderBottom: "1px solid var(--border-color)",
            padding: "0 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between"
          }}>
            <h2 style={{ fontSize: "18px", fontWeight: 600, color: "var(--text-primary)" }}>
              {activePage === "anomaly types" && "Anomaly Definitions"}
              {activePage === "heatmap" && "Geospatial Anomaly Heatmap"}
              {activePage === "analytics" && "Detailed Anomaly Analytics"}
              {activePage === "statewise" && "State-wise Reports"}
            </h2>
          </header>

          {/* Dynamic Content Container */}
          <div style={{ 
            flex: 1, 
            padding: "16px", 
            overflowY: "auto", // Allows scrolling for charts
            position: "relative"
          }}>
            {renderContent()}
          </div>
        </main>
      </div>
    </Provider>
  );
};

export default App;