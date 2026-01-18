import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { io } from "socket.io-client";
import type { RootState, AppDispatch } from "../store/store";
import { addAlert } from "../store/slices/alertsSlice";
import type { Alert } from "../store/slices/alertsSlice";

const SidePanel: React.FC = () => {
  const alerts = useSelector((state: RootState) => state.alerts.items);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    // Connect to Backend WebSocket
    const socket = io("http://localhost:8000");

    socket.on("new_alert", (data: any) => {
      const newAlert: Alert = {
        id: Date.now().toString(),
        type: data.type,
        pincode: data.pincode,
        message: data.message,
        timestamp: new Date().toLocaleTimeString(),
        severity: "CRITICAL",
      };
      dispatch(addAlert(newAlert));
    });

    return () => {
      socket.disconnect();
    };
  }, [dispatch]);

  return (
    <div
      className="card"
      style={{ height: "100%", display: "flex", flexDirection: "column" }}
    >
      <div
        style={{
          padding: "16px",
          borderBottom: "1px solid var(--border-color)",
        }}
      >
        <h2 style={{ fontSize: "var(--font-h2)", marginBottom: "4px" }}>
          Live Feed
        </h2>
        <p className="text-secondary text-small">Real-time detection log</p>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "0 16px" }}>
        {alerts.map((alert) => (
          <div
            key={alert.id}
            style={{
              padding: "12px 0",
              borderBottom: "1px solid var(--border-color)",
              display: "flex",
              flexDirection: "column",
              gap: "4px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span
                style={{
                  color: "var(--danger-color)",
                  fontWeight: 600,
                  fontSize: "var(--font-small)",
                }}
              >
                {alert.type.toUpperCase()}
              </span>
              <span className="text-secondary text-small">
                {alert.timestamp}
              </span>
            </div>
            <p style={{ fontSize: "var(--font-body-main)" }}>{alert.message}</p>
            <span className="text-secondary text-small">
              PIN: {alert.pincode}
            </span>
          </div>
        ))}
        {alerts.length === 0 && (
          <p
            style={{
              padding: "20px",
              textAlign: "center",
              color: "var(--text-secondary)",
            }}
          >
            System monitoring... No active alerts.
          </p>
        )}
      </div>
    </div>
  );
};

export default SidePanel;
