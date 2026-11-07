import type { ChartInstance, ChartLayout, ChartType } from "../types/charts";
import { create } from 'zustand'
import { persist } from "zustand/middleware";
import { immer } from "zustand/middleware/immer";
import { chartDefs } from "../constants/chartDefs";
import {nanoid} from 'nanoid'

interface DashboardState {
  charts: ChartInstance[],
  addChart: (type: ChartType) => void;
  removeChart: (id: string) => void;
  updateLayout: (layout: ChartLayout[]) => void;
}
function getNextPosition(charts: ChartInstance[]): Pick<ChartLayout, "x" | "y"> {
  if (charts.length === 0) return { x: 0, y: 0 };

  const maxY = Math.max(...charts.map((c) => c.layout.y + c.layout.h));
  return { x: 0, y: maxY };
}

export const useDashboardStore = create<DashboardState>()(
  persist(
    immer((set, get) => ({
      charts: [],

      addChart: (type) => {
        const def = chartDefs.find((d) => d.type === type);
        if (!def) {
          console.warn(`Unknown chart type: ${type}`);
          return;
        }

        const { w, h } = def.defaultLayout;
        const { x, y } = getNextPosition(get().charts);

        const newChart: ChartInstance = {
          id: nanoid(),
          type,
          layout: { id: "", x, y, w, h }
        };
        newChart.layout.id = newChart.id;

        set((state) => {
          state.charts.push(newChart);
        });
      },

      removeChart: (id) => {
        set((state) => {
          state.charts = state.charts.filter((c) => c.id !== id);
        });
      },

      updateLayout: (layout) => {
        set((state) => {
          for (const item of layout) {
            const chart = state.charts.find((c) => c.id === item.id);
            if (chart) {
              chart.layout = item;
            }
          }
        });
      },
    })),
    {
      name: "weather-dashboard-layout",
      partialize: (state) => ({ charts: state.charts }),
    }
  )
);
