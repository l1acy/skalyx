import json

from skalyx.adapters.parsers.base import ParsedMetric


class OpenWeatherMapParser:
    @staticmethod
    def parse(raw: str) -> list[ParsedMetric]:
        try:
            parsed = json.loads(raw)
        except ValueError:
            return []

        main_data = parsed.get('main')
        if not main_data:
            return []

        metrics = []

        if temp := main_data.get('temp'):
            metrics.append(
                ParsedMetric(
                    value=temp,
                    unit="C",
                    metric="temperature"
                )
            )
        if pressure := main_data.get('pressure'):
            metrics.append(
                ParsedMetric(
                    value=pressure,
                    unit="hPa",
                    metric="pressure"
                )
            )
        if humidity := main_data.get('humidity'):
            metrics.append(
                ParsedMetric(
                    value=humidity,
                    unit='%',
                    metric='humidity'
                )
            )

        return metrics
