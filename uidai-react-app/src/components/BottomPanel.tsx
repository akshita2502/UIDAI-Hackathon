import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

// Color Palette matching the map
const COLORS = {
  phantom: "#EF4444",
  update: "#F59E0B",
  bio: "#8B5CF6",
  ghost: "#3B82F6",
  bot: "#10B981",
  sunday: "#EC4899",
};

const BottomPanel: React.FC = () => {
  // State for each chart
  const [phantomData, setPhantomData] = useState([]);
  const [updateData, setUpdateData] = useState([]);
  const [bioData, setBioData] = useState([]);
  const [ghostData, setGhostData] = useState([]);
  const [botData, setBotData] = useState([]);
  const [sundayData, setSundayData] = useState([]);

  // Loading states for each chart
  const [loadingStates, setLoadingStates] = useState({
    phantom: true,
    update: true,
    bio: true,
    ghost: true,
    bot: true,
    sunday: true,
  });

  // Fetch Data on Load
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [res1, res2, res3, res4, res5, res6] = await Promise.all([
          axios.get("http://localhost:8000/analytics/phantom-village"),
          axios.get("http://localhost:8000/analytics/update-mill"),
          axios.get("http://localhost:8000/analytics/biometric-bypass"),
          axios.get("http://localhost:8000/analytics/scholarship-ghost"),
          axios.get("http://localhost:8000/analytics/bot-operator"),
          axios.get("http://localhost:8000/analytics/sunday-shift"),
        ]);

        setPhantomData(res1.data);
        setUpdateData(res2.data);
        setBioData(res3.data);
        setGhostData(res4.data);
        setBotData(res5.data);
        setSundayData(res6.data);

        // Mark all as loaded
        setLoadingStates({
          phantom: false,
          update: false,
          bio: false,
          ghost: false,
          bot: false,
          sunday: false,
        });
      } catch (err) {
        console.error("Chart data fetch error", err);
        // Mark all as not loading on error
        setLoadingStates({
          phantom: false,
          update: false,
          bio: false,
          ghost: false,
          bot: false,
          sunday: false,
        });
      }
    };
    fetchData();
  }, []);

  // Common Tooltip Style
  const tooltipStyle = {
    backgroundColor: "#fff",
    border: "1px solid #ccc",
    fontSize: "12px",
  };

  // Loader Component
  const Loader: React.FC = () => (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100%",
        gap: "12px",
      }}
    >
      <div
        style={{
          width: "30px",
          height: "30px",
          border: "3px solid #e5e7eb",
          borderTop: "3px solid #3b82f6",
          borderRadius: "50%",
          animation: "spin 1s linear infinite",
        }}
      />
      <p style={{ color: "#9ca3af", fontSize: "12px" }}>Loading chart...</p>
    </div>
  );

  return (
    <div style={{ height: "100%", overflowY: "auto", paddingRight: "8px" }}>
      {/* CSS for spinner animation */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>

      <h3
        style={{
          fontSize: "16px",
          marginBottom: "12px",
          color: "#495057",
          fontWeight: 700,
        }}
      >
        Detailed Anomaly Analytics
      </h3>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "16px",
          paddingBottom: "20px",
        }}
      >
        {/* 1. PHANTOM VILLAGE: Stacked Bar (State-wise) */}
        <div className="card" style={{ padding: "12px", height: "250px" }}>
          <h4
            style={{
              fontSize: "13px",
              color: COLORS.phantom,
              marginBottom: "8px",
            }}
          >
            1. Phantom Village (State Distribution)
          </h4>
          {loadingStates.phantom ? (
            <Loader />
          ) : (
            <ResponsiveContainer width="100%" height="90%">
              <BarChart data={phantomData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="state"
                  fontSize={10}
                  angle={-25}
                  textAnchor="end"
                  height={40}
                />
                <YAxis fontSize={10} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar
                  dataKey="normal_count"
                  stackId="a"
                  fill="#E5E7EB"
                  name="Normal"
                />
                <Bar
                  dataKey="anomaly_count"
                  stackId="a"
                  fill={COLORS.phantom}
                  name="Anomalies"
                />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 2. UPDATE MILL: Bar Chart (Suspicious Z-Scores) */}
        <div className="card" style={{ padding: "12px", height: "250px" }}>
          <h4
            style={{
              fontSize: "13px",
              color: COLORS.update,
              marginBottom: "8px",
            }}
          >
            2. Update Mill (Top Suspicious Districts)
          </h4>
          {loadingStates.update ? (
            <Loader />
          ) : (
            <ResponsiveContainer width="100%" height="90%">
              <BarChart data={updateData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" fontSize={10} />
                <YAxis
                  dataKey="district"
                  type="category"
                  width={80}
                  fontSize={9}
                />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar dataKey="z_score" fill={COLORS.update} name="Z-Score" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 3. BIOMETRIC BYPASS: Scatter Plot */}
        <div className="card" style={{ padding: "12px", height: "250px" }}>
          <h4
            style={{ fontSize: "13px", color: COLORS.bio, marginBottom: "8px" }}
          >
            3. Biometric Bypass (Correlation)
          </h4>
          {loadingStates.bio ? (
            <Loader />
          ) : (
            <ResponsiveContainer width="100%" height="90%">
              <ScatterChart>
                <CartesianGrid />
                <XAxis
                  type="number"
                  dataKey="demo_age_17_"
                  name="Demo Updates"
                  fontSize={10}
                />
                <YAxis
                  type="number"
                  dataKey="bio_age_17_"
                  name="Bio Updates"
                  fontSize={10}
                />
                <Tooltip
                  cursor={{ strokeDasharray: "3 3" }}
                  contentStyle={tooltipStyle}
                />
                <Scatter
                  name="Centers"
                  data={bioData}
                  fill={COLORS.bio}
                  shape="circle"
                />
              </ScatterChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 4. SCHOLARSHIP GHOST: Grouped Bar */}
        <div className="card" style={{ padding: "12px", height: "250px" }}>
          <h4
            style={{
              fontSize: "13px",
              color: COLORS.ghost,
              marginBottom: "8px",
            }}
          >
            4. Scholarship Ghost (Child Mismatch)
          </h4>
          {loadingStates.ghost ? (
            <Loader />
          ) : (
            <ResponsiveContainer width="100%" height="90%">
              <BarChart data={ghostData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="district"
                  fontSize={9}
                  interval={0}
                  angle={-25}
                  textAnchor="end"
                  height={40}
                />
                <YAxis fontSize={10} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar
                  dataKey="demo_age_5_17"
                  fill={COLORS.ghost}
                  name="Demographic"
                />
                <Bar dataKey="bio_age_5_17" fill="#93C5FD" name="Biometric" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 5. BOT OPERATOR: Pie Chart */}
        <div className="card" style={{ padding: "12px", height: "250px" }}>
          <h4
            style={{ fontSize: "13px", color: COLORS.bot, marginBottom: "8px" }}
          >
            5. Bot Operator (Round Number %)
          </h4>
          {loadingStates.bot ? (
            <Loader />
          ) : (
            <ResponsiveContainer width="100%" height="90%">
              <PieChart>
                <Pie
                  data={botData}
                  cx="50%"
                  cy="50%"
                  outerRadius={60}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ percent }) =>
                    `${(percent !== undefined ? (percent * 100).toFixed(0) : 0)}%`
                  }
                >
                  {botData.map((_entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={index === 0 ? COLORS.bot : "#E5E7EB"}
                    />
                  ))}
                </Pie>
                <Tooltip contentStyle={tooltipStyle} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 6. SUNDAY SHIFT: Line Chart */}
        <div className="card" style={{ padding: "12px", height: "250px" }}>
          <h4
            style={{
              fontSize: "13px",
              color: COLORS.sunday,
              marginBottom: "8px",
            }}
          >
            6. Sunday Shift (Weekly Trend)
          </h4>
          {loadingStates.sunday ? (
            <Loader />
          ) : (
            <ResponsiveContainer width="100%" height="90%">
              <LineChart data={sundayData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day_of_week" fontSize={10} />
                <YAxis fontSize={10} />
                <Tooltip contentStyle={tooltipStyle} />
                <Line
                  type="monotone"
                  dataKey="age_18_greater"
                  stroke={COLORS.sunday}
                  strokeWidth={2}
                  name="Avg Adult Enrolment"
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  );
};

export default BottomPanel;
