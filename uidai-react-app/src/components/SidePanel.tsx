import React from "react";

interface SidePanelProps {
  activePage: string;
  onNavigate: (page: string) => void;
}

const SidePanel: React.FC<SidePanelProps> = ({ activePage, onNavigate }) => {
  const menuItems = [
    {id: "anomaly types", label: "Anomaly Types", icon: "⚠️" },
    { id: "heatmap", label: "Aadhar HeatMap", icon: "🗺️" },
    { id: "analytics", label: "Anomaly Analytics", icon: "📊" },
    { id: "statewise", label: "State-wise Analytics", icon: "🇮🇳" },
  ];

  return (
    <div
      style={{
        width: "260px",
        backgroundColor: "#FFFFFF",
        borderRight: "1px solid var(--border-color)",
        display: "flex",
        flexDirection: "column",
        height: "100%",
        zIndex: 10
      }}
    >
      {/* Logo Area */}
      <div style={{ padding: "24px", borderBottom: "1px solid var(--border-color)" }}>
        <h1 style={{ fontSize: "20px", color: "var(--accent-color)", margin: 0, fontWeight: 800 }}>
          UIDAI SENTINEL
        </h1>
        <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "4px" }}>
          Fraud Detection System
        </div>
      </div>

      {/* Navigation Menu */}
      <nav style={{ flex: 1, padding: "16px" }}>
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            style={{
              width: "100%",
              display: "flex",
              alignItems: "center",
              gap: "12px",
              padding: "12px 16px",
              marginBottom: "8px",
              border: "none",
              borderRadius: "8px",
              backgroundColor: activePage === item.id ? "#EFF6FF" : "transparent",
              color: activePage === item.id ? "var(--accent-color)" : "var(--text-primary)",
              cursor: "pointer",
              textAlign: "left",
              fontWeight: activePage === item.id ? 600 : 500,
              transition: "all 0.2s"
            }}
          >
            <span style={{ fontSize: "18px" }}>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Footer Status */}
      <div style={{ padding: "16px", borderTop: "1px solid var(--border-color)", backgroundColor: "#F8F9FA" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "12px", color: "var(--text-secondary)" }}>
          <div style={{ width: "8px", height: "8px", borderRadius: "50%", backgroundColor: "var(--success-color)" }}></div>
          System Operational
        </div>
      </div>
    </div>
  );
};

export default SidePanel;