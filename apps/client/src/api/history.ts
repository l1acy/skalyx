// api/weather.ts
import { apiFetch } from './client';

interface WeatherRecord {
    device_id: string;
    source: string;
    metric: string;
    value: any;
    unit: string;
    timestamp: string;
    meta: object;
}

type WeatherResponse = WeatherRecord[]

export function fetchHistory() {
  return apiFetch<WeatherResponse>(`/history`);
}