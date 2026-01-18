import { configureStore } from "@reduxjs/toolkit";
import alertsReducer from "./slices/alertsSlice";

export const store = configureStore({
  reducer: {
    alerts: alertsReducer,
    // analytics: analyticsReducer (Add later if needed)
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
