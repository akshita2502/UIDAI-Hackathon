import React from "react";
import { Provider } from "react-redux";
import { store } from "./store/store";
import TopBar from "./components/TopBar";
import MainPanel from "./components/MainPanel";
import SidePanel from "./components/SidePanel";
import BottomPanel from "./components/BottomPanel";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div
        style={{ height: "100vh", display: "flex", flexDirection: "column" }}
      >
        <TopBar />

        <div
          style={{
            flex: 1,
            padding: "16px",
            display: "grid",
            gridTemplateColumns: "12fr 4fr", // 75% Map/Charts, 25% Sidebar
            gridTemplateRows: "2fr 1fr", // 66% Map, 33% Charts
            gap: "16px",
            overflow: "hidden",
          }}
        >
          {/* Main Panel (Map) - Spans 1st column, 1st row */}
          <div style={{ gridColumn: "1 / 2", gridRow: "1 / 2" }}>
            <MainPanel />
          </div>

          {/* Side Panel (Feed) - Spans 2nd column, both rows (Full Height) */}
          <div style={{ gridColumn: "2 / 3", gridRow: "1 / 3" }}>
            <SidePanel />
          </div>

          {/* Bottom Panel (Charts) - Spans 1st column, 2nd row */}
          <div style={{ gridColumn: "1 / 2", gridRow: "2 / 3" }}>
            <BottomPanel />
          </div>
        </div>
      </div>
    </Provider>
  );
};

export default App;
