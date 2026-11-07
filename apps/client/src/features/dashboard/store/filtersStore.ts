type DateRange = {
  from: Date | undefined;
  to: Date | undefined;
};

export interface FiltersState {
  range: { from: Date, to: Date };
  stepMinutes: 10 | 30 | 60 | 90;
  units: {
    tempretaure: 'celsius' | 'fahrenheit',
    wind: 'ms' | 'kmh' | 'mph',
    pressure: 'hpa' | 'mmhg'
  },
  setRange: (range: DateRange) => void;
  setStep: (step: number) => void;
  setUnit: (key: string, value: string) => void;
}
