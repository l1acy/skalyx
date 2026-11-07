import { useState } from "react";
import { Responsive, useContainerWidth } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";

const BREAKPOINTS = { lg: 1200, md: 996, sm: 768, xs: 480 };
const COLS = { lg: 12, md: 10, sm: 6, xs: 4 };

const MOCK_CHARTS = [
  { id: "1", label: "Температура", color: "bg-red-200", layout: { x: 0, y: 0, w: 4, h: 3 } },
  { id: "2", label: "Влажность", color: "bg-blue-200", layout: { x: 4, y: 0, w: 4, h: 3 } },
  { id: "3", label: "Ветер", color: "bg-green-200", layout: { x: 8, y: 0, w: 4, h: 3 } },
  { id: "4", label: "Давление", color: "bg-yellow-200", layout: { x: 0, y: 3, w: 6, h: 3 } },
  { id: "5", label: "Осадки", color: "bg-purple-200", layout: { x: 6, y: 3, w: 6, h: 3 } },
];

export default function DashboardGrid() {
  const [charts, setCharts] = useState(MOCK_CHARTS);
  const { width, containerRef, mounted } = useContainerWidth();

  const rglLayout = charts.map((chart) => ({
    i: chart.id,
    x: chart.layout.x,
    y: chart.layout.y,
    w: chart.layout.w,
    h: chart.layout.h,
    minW: 2,
    minH: 2,
  }));

  const layouts = { lg: rglLayout, md: rglLayout, sm: rglLayout, xs: rglLayout };

  const handleLayoutChange = (layout: typeof rglLayout) => {
    setCharts((prev) =>
      prev.map((chart) => {
        const updated = layout.find((l) => l.i === chart.id);
        return updated
          ? { ...chart, layout: { x: updated.x, y: updated.y, w: updated.w, h: updated.h } }
          : chart;
      })
    );
  };

  const removeChart = (id: string) => setCharts((prev) => prev.filter((c) => c.id !== id));

  const addChart = () => {
    const id = crypto.randomUUID();
    const colors = ["bg-red-200", "bg-blue-200", "bg-green-200", "bg-yellow-200", "bg-purple-200"];
    setCharts((prev) => [
      ...prev,
      { id, label: `Новый график ${prev.length + 1}`, color: colors[Math.floor(Math.random() * colors.length)], layout: { x: 0, y: Infinity, w: 4, h: 3 } },
    ]);
  };

  return (
    <div className="space-y-4">
      <button onClick={addChart} className="rounded-md border px-3 py-1.5 text-sm hover:bg-accent">
        + Добавить график
      </button>

      <div ref={containerRef} style={{ width: "100%" }}>
        {mounted && (
          <Responsive
            layouts={layouts}
            breakpoints={BREAKPOINTS}
            cols={COLS}
            margin={[16, 16]}
            width={width}
            rowHeight={80}
            dragConfig={{ handle: ".chart-drag-handle" }}
            onLayoutChange={() => handleLayoutChange}
          >
            {charts.map((chart) => (
              <div key={chart.id}>
                <div className={`flex h-full w-full flex-col rounded-lg border ${chart.color}`}>
                  <div className="chart-drag-handle flex cursor-move items-center justify-between rounded-t-lg bg-black/10 px-3 py-1.5">
                    <span className="text-sm font-medium">{chart.label}</span>
                    <button onClick={() => removeChart(chart.id)} className="text-sm text-black/60 hover:text-black">✕</button>
                  </div>
                  <div className="flex flex-1 items-center justify-center text-xs text-black/40">{chart.id}</div>
                </div>
              </div>
            ))}
          </Responsive>
        )}
      </div>
    </div>
  );
}
