import React from "react";
import { useSelector } from "react-redux";
import type { RootState } from "../store/store";

const TopBar: React.FC = () => {
  const totalAnomalies = useSelector(
    (state: RootState) => state.alerts.totalToday,
  );

  return (
    <header
      style={{
        height: "var(--header-height)",
        backgroundColor: "var(--surface-color)",
        borderBottom: "1px solid var(--border-color)",
        padding: "0 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <h1
          style={{ fontSize: "var(--font-h2)", color: "var(--accent-color)" }}
        >
          UIDAI SENTINEL
        </h1>
        <div
          style={{
            backgroundColor: "#FFF5F5",
            border: "1px solid var(--danger-color)",
            color: "var(--danger-color)",
            padding: "6px 12px",
            borderRadius: "20px",
            fontSize: "var(--font-small)",
            fontWeight: 600,
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <span
            style={{
              width: "8px",
              height: "8px",
              borderRadius: "50%",
              backgroundColor: "var(--danger-color)",
              animation: "pulse 1.5s infinite",
            }}
          />
          LIVE THREATS: {totalAnomalies}
        </div>
      </div>

      <div
        style={{
          fontSize: "var(--font-small)",
          color: "var(--text-secondary)",
        }}
      >
        System Status:{" "}
        <span style={{ color: "var(--success-color)", fontWeight: 600 }}>
          OPERATIONAL
        </span>
      </div>
    </header>
  );
};

export default TopBar;
