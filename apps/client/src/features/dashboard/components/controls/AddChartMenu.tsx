import { Button } from "@/components/ui/button";
import { chartDefs } from "../../constants/chartDefs";
import { useDashboardStore } from "../../store/dashboardStore";

export function AddChartMenu() {
  const addChart = useDashboardStore(s => s.addChart);

  return (
    <>
      {chartDefs.map((def) => (
        <Button key={def.type} onClick={() => addChart(def.type)}>{def.label ?? def.type}</Button>
      ))}
    </>
  );
}
