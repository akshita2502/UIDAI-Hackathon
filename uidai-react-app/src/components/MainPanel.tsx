import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix for default marker icons in Leaflet with React
// (Though we use CircleMarkers, this prevents 404s if you add standard markers later)
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

// --- CONFIGURATION ---

const ANOMALY_THEMES: Record<string, { color: string; label: string }> = {
  "Phantom Village": { color: "#EF4444", label: "Fake ID Ring" },
  "Update Mill": { color: "#F59E0B", label: "Bulk Operations" },
  "Biometric Bypass": { color: "#8B5CF6", label: "Incomplete Verification" },
  "Scholarship Ghost": { color: "#3B82F6", label: "Child Age Mismatch" },
  "Bot Operator": { color: "#10B981", label: "Pattern Fabrication" },
  "Sunday Shift": { color: "#EC4899", label: "Temporal Fraud" },
};

interface MapPoint {
  pincode: number;
  district: string;
  state: string;
  lat: number;
  lng: number;
  type: string;
  // Dynamic fields based on anomaly type
  age_18_greater?: number;
  z_score?: number;
  risk_score?: number;
  round_pct?: number;
}

// --- SUB-COMPONENTS ---

// Automatically zooms/pans to fit all markers
const MapAutoCenter = ({ points }: { points: MapPoint[] }) => {
  const map = useMap();
  useEffect(() => {
    if (points.length > 0) {
      const bounds = L.latLngBounds(points.map((p) => [p.lat, p.lng]));
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [points, map]);
  return null;
};

const MainPanel: React.FC = () => {
  const [points, setPoints] = useState<MapPoint[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch("http://localhost:8000/analytics/map-all")
      .then((res) => res.json())
      .then((data) => {
        setPoints(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Map Ingestion Error:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div
      className="card"
      style={{
        height: "100%",
        position: "relative",
        overflow: "hidden",
        borderRadius: "12px",
      }}
    >
      {/* HEADER OVERLAY */}
      <div
        style={{
          position: "absolute",
          top: 16,
          left: 16,
          zIndex: 1000,
          backgroundColor: "rgba(255,255,255,0.95)",
          padding: "8px 12px",
          borderRadius: "6px",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          fontSize: "14px",
          fontWeight: 600,
          color: "#1F2937",
        }}
      >
        Geospatial Anomaly View
        {loading && (
          <span
            style={{ marginLeft: "8px", fontSize: "12px", color: "#6B7280" }}
          >
            (Loading...)
          </span>
        )}
      </div>

      {/* LEGEND OVERLAY */}
      <div
        style={{
          position: "absolute",
          bottom: 24,
          right: 24,
          zIndex: 1000,
          backgroundColor: "rgba(255,255,255,0.95)",
          padding: "16px",
          borderRadius: "8px",
          boxShadow:
            "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
          border: "1px solid #E5E7EB",
          minWidth: "200px",
        }}
      >
        <h4
          style={{
            margin: "0 0 12px 0",
            fontSize: "12px",
            textTransform: "uppercase",
            color: "#6B7280",
            fontWeight: 700,
          }}
        >
          Anomaly Key
        </h4>
        <div
          style={{ display: "grid", gridTemplateColumns: "1fr", gap: "8px" }}
        >
          {Object.entries(ANOMALY_THEMES).map(([type, theme]) => (
            <div
              key={type}
              style={{ display: "flex", alignItems: "center", gap: "8px" }}
            >
              <span
                style={{
                  width: "12px",
                  height: "12px",
                  borderRadius: "50%",
                  backgroundColor: theme.color,
                  display: "inline-block",
                  boxShadow: "0 0 0 2px rgba(255,255,255,1)",
                }}
              />
              <div style={{ display: "flex", flexDirection: "column" }}>
                <span
                  style={{
                    fontSize: "12px",
                    fontWeight: 600,
                    color: "#374151",
                  }}
                >
                  {type}
                </span>
                <span style={{ fontSize: "10px", color: "#9CA3AF" }}>
                  {theme.label}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* MAP CONTAINER */}
      <MapContainer
        center={[20.5937, 78.9629]}
        zoom={5}
        style={{ height: "100%", width: "100%", zIndex: 0 }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        <MapAutoCenter points={points} />

        {points.map((pt, idx) => {
          const theme = ANOMALY_THEMES[pt.type] || {
            color: "#333",
            label: "Unknown",
          };
          return (
            <CircleMarker
              key={`${pt.pincode}-${idx}`}
              center={[pt.lat, pt.lng]}
              radius={8}
              pathOptions={{
                fillColor: theme.color,
                color: "white",
                weight: 2,
                fillOpacity: 0.8,
              }}
            >
              <Popup>
                <div style={{ minWidth: "150px", padding: "4px" }}>
                  <div
                    style={{
                      fontSize: "12px",
                      fontWeight: 700,
                      color: theme.color,
                      textTransform: "uppercase",
                      marginBottom: "4px",
                      borderBottom: `2px solid ${theme.color}`,
                      paddingBottom: "4px",
                    }}
                  >
                    {pt.type}
                  </div>

                  <div
                    style={{
                      fontSize: "12px",
                      color: "#374151",
                      lineHeight: "1.6",
                    }}
                  >
                    <div>
                      <strong>District:</strong> {pt.district}
                    </div>
                    <div>
                      <strong>State:</strong> {pt.state}
                    </div>
                    <div>
                      <strong>PIN:</strong> {pt.pincode}
                    </div>

                    {/* Conditional Metadata Display */}
                    {pt.age_18_greater && (
                      <div
                        style={{
                          marginTop: "6px",
                          backgroundColor: "#F3F4F6",
                          padding: "4px",
                          borderRadius: "4px",
                        }}
                      >
                        Adult Vol: <strong>{pt.age_18_greater}</strong>
                      </div>
                    )}
                    {pt.z_score && (
                      <div
                        style={{
                          marginTop: "6px",
                          backgroundColor: "#F3F4F6",
                          padding: "4px",
                          borderRadius: "4px",
                        }}
                      >
                        Z-Score: <strong>{pt.z_score.toFixed(2)}</strong>
                      </div>
                    )}
                    {pt.risk_score && (
                      <div
                        style={{
                          marginTop: "6px",
                          backgroundColor: "#F3F4F6",
                          padding: "4px",
                          borderRadius: "4px",
                        }}
                      >
                        Risk Score: <strong>{pt.risk_score.toFixed(2)}</strong>
                      </div>
                    )}
                    {pt.round_pct && (
                      <div
                        style={{
                          marginTop: "6px",
                          backgroundColor: "#F3F4F6",
                          padding: "4px",
                          borderRadius: "4px",
                        }}
                      >
                        Round Number %:{" "}
                        <strong>{pt.round_pct.toFixed(1)}%</strong>
                      </div>
                    )}
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default MainPanel;
