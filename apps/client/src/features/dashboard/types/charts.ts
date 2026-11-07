export interface ChartLayout {
  id: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface ChartInstance {
  id: string,
  type: ChartType,
  layout: ChartLayout,
}

export const CHART_TYPES = [
  'temperature',
  'humidity',
  'wind',
  'pressure',
  'precipitation',
  'uv-index',
] as const;

export type ChartType = typeof CHART_TYPES[number];

export interface ChartDefinition {
  type: ChartType;
  label: string;
  defaultLayout: Pick<ChartLayout, 'w' | 'h'>;
}
