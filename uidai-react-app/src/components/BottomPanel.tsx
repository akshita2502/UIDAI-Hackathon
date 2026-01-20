import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
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
  const [phantomData, setPhantomData] = useState<any[]>([]);
  const [updateData, setUpdateData] = useState<any[]>([]);
  const [bioData, setBioData] = useState<any[]>([]);
  const [ghostData, setGhostData] = useState<any[]>([]);
  const [botData, setBotData] = useState<any[]>([]);
  const [sundayData, setSundayData] = useState<any[]>([]);

  // Fetch Data on Load
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [res1, res2, res3, res4, res5, res6] = await Promise.all([
          fetch("http://localhost:8000/analytics/phantom-village"),
          fetch("http://localhost:8000/analytics/update-mill"),
          fetch("http://localhost:8000/analytics/biometric-bypass"),
          fetch("http://localhost:8000/analytics/scholarship-ghost"),
          fetch("http://localhost:8000/analytics/bot-operator"),
          fetch("http://localhost:8000/analytics/sunday-shift"),
        ]);

        setPhantomData(await res1.json());
        setUpdateData(await res2.json());
        setBioData(await res3.json());
        setGhostData(await res4.json());
        setBotData(await res5.json());
        setSundayData(await res6.json());
      } catch (err) {
        console.error("Chart data fetch error", err);
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

  // Chart Title Style
  const chartTitleStyle = {
    fontSize: "14px",
    fontWeight: 700,
    marginBottom: "16px",
    display: "flex",
    alignItems: "center",
    gap: "8px",
  };

  return (
    <div style={{ height: "100%", overflowY: "auto", paddingRight: "8px" }}>
      {/* Container: Flex Column for Full Width Stacking */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "24px",
          paddingBottom: "32px",
        }}
      >
        {/* 1. PHANTOM VILLAGE: Stacked Bar (State-wise) WITH SCROLL */}
        <div
          className="card"
          style={{
            padding: "20px",
            height: "420px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{ ...chartTitleStyle, color: COLORS.phantom, flexShrink: 0 }}
          >
            <span
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: COLORS.phantom,
                borderRadius: "50%",
              }}
            ></span>
            1. Phantom Village (State Distribution)
          </div>

          <div
            style={{
              flex: 1,
              overflowX: "auto",
              overflowY: "hidden",
              border: "1px solid #f0f0f0",
              borderRadius: "4px",
            }}
          >
            {/* dynamic width ensuring ~60px per state for readability */}
            <div
              style={{
                width: `${Math.max(100, phantomData.length * 60)}px`,
                height: "100%",
                minWidth: "100%",
              }}
            >
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={phantomData}
                  margin={{ top: 10, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="state"
                    fontSize={11}
                    interval={0}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    tickFormatter={(val) =>
                      val.length > 15 ? `${val.substring(0, 15)}...` : val
                    }
                  />
                  <YAxis fontSize={11} />
                  {/* FIX: cursor={{ fill: 'transparent' }} removes the grey background */}
                  <Tooltip
                    contentStyle={tooltipStyle}
                    cursor={{ fill: "transparent" }}
                  />
                  <Legend verticalAlign="top" height={36} />
                  <Bar
                    dataKey="normal_count"
                    stackId="a"
                    fill="#a7aaae"
                    name="Normal Enrolments"
                    barSize={30}
                  />
                  <Bar
                    dataKey="anomaly_count"
                    stackId="a"
                    fill={COLORS.phantom}
                    name="Anomalies"
                    barSize={30}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div
            style={{
              fontSize: "10px",
              color: "#999",
              textAlign: "center",
              marginTop: "4px",
            }}
          >
            Scroll horizontally to view all states →
          </div>
        </div>

        {/* 2. UPDATE MILL: Bar Chart (Suspicious Z-Scores) */}
        <div className="card" style={{ padding: "20px", height: "350px" }}>
          <div style={{ ...chartTitleStyle, color: COLORS.update }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: COLORS.update,
                borderRadius: "50%",
              }}
            ></span>
            2. Update Mill (Top Suspicious Districts)
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart
              data={updateData}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" fontSize={11} />
              <YAxis
                dataKey="district"
                type="category"
                width={120}
                fontSize={11}
              />
              <Tooltip
                contentStyle={tooltipStyle}
                cursor={{ fill: "transparent" }}
              />
              <Legend verticalAlign="top" height={36} />
              <Bar
                dataKey="z_score"
                fill={COLORS.update}
                name="Z-Score (Deviation)"
                barSize={20}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 3. BIOMETRIC BYPASS: Grouped Bar Chart (State-wise) */}
        <div className="card" style={{ padding: "20px", height: "350px" }}>
          <div style={{ ...chartTitleStyle, color: COLORS.bio }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: COLORS.bio,
                borderRadius: "50%",
              }}
            ></span>
            3. Biometric Bypass (State-wise Verification Gap)
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart
              data={bioData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="state"
                fontSize={11}
                interval={0}
                angle={-15}
                textAnchor="end"
                height={60}
                tickFormatter={(val) =>
                  val.length > 10 ? `${val.substring(0, 10)}..` : val
                }
              />
              <YAxis fontSize={11} />
              <Tooltip
                cursor={{ fill: "transparent" }}
                contentStyle={{
                  backgroundColor: "#fff",
                  border: "1px solid #ccc",
                  fontSize: "12px",
                }}
              />
              <Legend verticalAlign="top" height={36} />

              {/* Bar 1: Demographic Updates (The Risk) */}
              <Bar
                dataKey="demo_age_17_"
                name="Demographic Updates"
                fill={COLORS.bio}
                barSize={20}
                radius={[4, 4, 0, 0]}
              />

              {/* Bar 2: Biometric Updates (The Verification) */}
              <Bar
                dataKey="bio_age_17_"
                name="Biometric Updates"
                fill="#C4B5FD" /* Lighter purple for contrast */
                barSize={20}
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 4. SCHOLARSHIP GHOST: Grouped Bar */}
        <div className="card" style={{ padding: "20px", height: "350px" }}>
          <div style={{ ...chartTitleStyle, color: COLORS.ghost }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: COLORS.ghost,
                borderRadius: "50%",
              }}
            ></span>
            4. Scholarship Ghost (Child Mismatch)
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart
              data={ghostData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="district"
                fontSize={11}
                interval={0}
                angle={-15}
                textAnchor="end"
                height={60}
              />
              <YAxis fontSize={11} />
              <Tooltip
                contentStyle={tooltipStyle}
                cursor={{ fill: "transparent" }}
              />
              <Legend verticalAlign="top" height={36} />
              <Bar
                dataKey="demo_age_5_17"
                fill={COLORS.ghost}
                name="Demographic Updates (Child)"
              />
              <Bar
                dataKey="bio_age_5_17"
                fill="#93C5FD"
                name="Biometric Updates (Child)"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 5. BOT OPERATOR: Pie Chart */}
        <div className="card" style={{ padding: "20px", height: "350px" }}>
          <div style={{ ...chartTitleStyle, color: COLORS.bot }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: COLORS.bot,
                borderRadius: "50%",
              }}
            ></span>
            5. Bot Operator (Round Number Analysis)
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <PieChart>
              <Pie
                data={botData}
                cx="50%"
                cy="50%"
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
                label={({ name, percent }) =>
                  `${name}: ${((percent ?? 0) * 100).toFixed(0)}%`
                }
              >
                {botData.map((_, index) => (
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
        </div>

        {/* 6. SUNDAY SHIFT: Line Chart */}
        <div className="card" style={{ padding: "20px", height: "350px" }}>
          <div style={{ ...chartTitleStyle, color: COLORS.sunday }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                backgroundColor: COLORS.sunday,
                borderRadius: "50%",
              }}
            ></span>
            6. Sunday Shift (Weekly Trend)
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart
              data={sundayData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day_of_week" fontSize={11} />
              <YAxis fontSize={11} />
              <Tooltip contentStyle={tooltipStyle} />
              <Legend verticalAlign="top" height={36} />
              <Line
                type="monotone"
                dataKey="age_18_greater"
                stroke={COLORS.sunday}
                strokeWidth={3}
                activeDot={{ r: 8 }}
                name="Avg Adult Enrolment Volume"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default BottomPanel;
