import React, { useEffect, useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// 1. Define Anomaly Types and Colors
const ANOMALY_COLORS: Record<string, string> = {
  "Phantom Village": "#EF4444", // Red
  "Update Mill": "#F59E0B", // Orange
  "Biometric Bypass": "#8B5CF6", // Purple
  "Scholarship Ghost": "#3B82F6", // Blue
  "Bot Operator": "#10B981", // Green
  "Sunday Shift": "#EC4899", // Pink
};

interface MapPoint {
  pincode: number;
  district: string;
  state: string;
  lat: number;
  lng: number;
  type: string; // The Anomaly Type
  age_18_greater?: number;
  z_score?: number;
}

const MainPanel: React.FC = () => {
  const [points, setPoints] = useState<MapPoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch aggregated map data
    setLoading(true);
    axios
      .get("http://localhost:8000/analytics/map-all")
      .then((res) => {
        setPoints(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Map fetch error:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div
      className="card"
      style={{ height: "100%", position: "relative", overflow: "hidden" }}
    >
      {/* Loading Overlay */}
      {loading && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(255, 255, 255, 0.9)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              width: "40px",
              height: "40px",
              border: "4px solid #e5e7eb",
              borderTop: "4px solid #3b82f6",
              borderRadius: "50%",
              animation: "spin 1s linear infinite",
            }}
          />
          <p style={{ marginTop: "16px", color: "#6b7280", fontSize: "14px" }}>
            Loading anomalies...
          </p>
        </div>
      )}

      {/* CSS for spinner animation */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
      {/* Title Overlay */}
      <div
        style={{
          position: "absolute",
          top: 16,
          left: 16,
          zIndex: 999,
          backgroundColor: "rgba(255,255,255,0.95)",
          padding: "8px 12px",
          borderRadius: 6,
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          fontSize: "var(--font-small)",
          fontWeight: 600,
        }}
      >
        Geospatial Anomaly View
      </div>

      {/* LEGEND OVERLAY */}
      <div
        style={{
          position: "absolute",
          bottom: 20,
          right: 20,
          zIndex: 999,
          backgroundColor: "rgba(255,255,255,0.95)",
          padding: "12px",
          borderRadius: 8,
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
          minWidth: "180px",
        }}
      >
        <h4 style={{ margin: "0 0 8px 0", fontSize: "12px", color: "#666" }}>
          ANOMALY KEY
        </h4>
        {Object.entries(ANOMALY_COLORS).map(([type, color]) => (
          <div
            key={type}
            style={{
              display: "flex",
              alignItems: "center",
              marginBottom: "4px",
            }}
          >
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "50%",
                backgroundColor: color,
                marginRight: "8px",
                display: "inline-block",
              }}
            />
            <span style={{ fontSize: "11px", fontWeight: 500 }}>{type}</span>
          </div>
        ))}
      </div>

      <MapContainer
        center={[22.5937, 78.9629]}
        zoom={5}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {points.map((pt, idx) => (
          <CircleMarker
            key={`${pt.pincode}-${idx}`}
            center={[pt.lat, pt.lng]}
            radius={6}
            pathOptions={{
              color: "white",
              weight: 1,
              fillColor: ANOMALY_COLORS[pt.type] || "#333",
              fillOpacity: 0.8,
            }}
          >
            <Popup>
              <div style={{ fontSize: "12px" }}>
                <strong style={{ color: ANOMALY_COLORS[pt.type] }}>
                  {pt.type.toUpperCase()}
                </strong>
                <br />
                District: {pt.district}, {pt.state}
                <br />
                Pincode: {pt.pincode}
                <br />
                {pt.age_18_greater && (
                  <span>Adult Vol: {pt.age_18_greater}</span>
                )}
                {pt.z_score && <span>Z-Score: {pt.z_score.toFixed(2)}</span>}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MainPanel;
