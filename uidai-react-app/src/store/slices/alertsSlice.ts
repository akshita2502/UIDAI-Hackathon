import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

export interface Alert {
  id: string;
  type: string; // e.g., "Phantom Village"
  pincode: number;
  message: string;
  timestamp: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM";
}

interface AlertsState {
  items: Alert[];
  totalToday: number;
}

const initialState: AlertsState = {
  items: [],
  totalToday: 0,
};

const alertsSlice = createSlice({
  name: "alerts",
  initialState,
  reducers: {
    addAlert: (state, action: PayloadAction<Alert>) => {
      // Add new alert to the top of the list
      state.items.unshift(action.payload);
      state.totalToday += 1;
    },
    setTotalAnomalies: (state, action: PayloadAction<number>) => {
      state.totalToday = action.payload;
    },
  },
});

export const { addAlert, setTotalAnomalies } = alertsSlice.actions;
export default alertsSlice.reducer;
