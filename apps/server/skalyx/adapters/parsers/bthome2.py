from dataclasses import dataclass

from .base import ParsedMetric

SERVICE_DATA_UUID = "0000fcd2-0000-1000-8000-00805f9b34fb"


_TEXT_OBJECT_ID = 0x53

_LENGTH_1 = {
    0x00, 0x01, 0x09, 0x0F, 0x10, 0x11, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A,
    0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26,
    0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x46, 0x57, 0x58,
    0x59, 0x60,
}
_LENGTH_2 = {
    0x02, 0x03, 0x06, 0x07, 0x08, 0x0C, 0x0D, 0x0E, 0x12, 0x13, 0x14, 0x3D,
    0x3F, 0x40, 0x41, 0x43, 0x44, 0x45, 0x47, 0x48, 0x49, 0x4A, 0x51, 0x52,
    0x56, 0x5A, 0x5D, 0x5E, 0x5F, 0x61, 0xF0,
}
_LENGTH_3 = {0x04, 0x05, 0x0A, 0x0B, 0x42, 0x4B, 0xF2}
_LENGTH_4 = {0x3E, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x55, 0x5B, 0x5C, 0x62, 0x63, 0xF1}

LENGTH_TABLE: dict[int, int] = {
    **{i: 1 for i in _LENGTH_1},
    **{i: 2 for i in _LENGTH_2},
    **{i: 3 for i in _LENGTH_3},
    **{i: 4 for i in _LENGTH_4},
}


@dataclass(frozen=True)
class _ObjectSpec:
    metric: str
    signed: bool
    factor: float
    unit: str | None
    is_bool: bool = False

# All device types: https://bthome.io/format/
SEMANTIC_TABLE: dict[int, _ObjectSpec] = {
    # —— Misc / internal ——————————————————————————————————————————————————
    0x00: _ObjectSpec("packet_id",         False, 1,        None),
    0xF0: _ObjectSpec("device_type_id",    False, 1,        None),
    0xF1: _ObjectSpec("firmware_version",  False, 1,        None),
    0xF2: _ObjectSpec("firmware_version",  False, 1,        None),

    # —— Number sensors ———————————————————————————————————————————————————
    0x01: _ObjectSpec("battery",             False, 1,        "%"),
    0x02: _ObjectSpec("temperature",         True,  0.01,     "C"),
    0x03: _ObjectSpec("humidity",            False, 0.01,     "%"),
    0x04: _ObjectSpec("pressure",            False, 0.01,     "hPa"),
    0x05: _ObjectSpec("illuminance",         False, 0.01,     "lx"),
    0x06: _ObjectSpec("mass_kg",             False, 0.01,     "kg"),
    0x07: _ObjectSpec("mass_lb",             False, 0.01,     "lb"),
    0x08: _ObjectSpec("dewpoint",            True,  0.01,     "C"),
    0x09: _ObjectSpec("count",               False, 1,        None),
    0x0A: _ObjectSpec("energy",              False, 0.001,    "kWh"),
    0x0B: _ObjectSpec("power",               False, 0.01,     "W"),
    0x0C: _ObjectSpec("voltage",             False, 0.001,    "V"),
    0x0D: _ObjectSpec("pm2_5",               False, 1,        "ug/m3"),
    0x0E: _ObjectSpec("pm10",                False, 1,        "ug/m3"),
    0x12: _ObjectSpec("co2",                 False, 1,        "ppm"),
    0x13: _ObjectSpec("tvoc",                False, 1,        "ug/m3"),
    0x14: _ObjectSpec("moisture",            False, 0.01,     "%"),
    0x2E: _ObjectSpec("humidity_coarse",     False, 1,        "%"),
    0x2F: _ObjectSpec("moisture_coarse",     False, 1,        "%"),
    0x3D: _ObjectSpec("count_2",             False, 1,        None),
    0x3E: _ObjectSpec("count_4",             False, 1,        None),
    0x3F: _ObjectSpec("rotation",            True,  0.1,      "°"),
    0x40: _ObjectSpec("distance_mm",         False, 1,        "mm"),
    0x41: _ObjectSpec("distance_m",          False, 0.1,      "m"),
    0x42: _ObjectSpec("duration",            False, 0.001,    "s"),
    0x43: _ObjectSpec("current",             False, 0.001,    "A"),
    0x44: _ObjectSpec("speed",               False, 0.01,     "m/s"),
    0x45: _ObjectSpec("temperature_coarse",  True,  0.1,      "C"),
    0x46: _ObjectSpec("uv_index",            False, 0.1,      None),
    0x47: _ObjectSpec("volume",              False, 0.1,      "L"),
    0x48: _ObjectSpec("volume_mL",           False, 1,        "mL"),
    0x49: _ObjectSpec("volume_flow_rate",    False, 0.001,    "m3/hr"),
    0x4A: _ObjectSpec("voltage_coarse",      False, 0.1,      "V"),
    0x4B: _ObjectSpec("gas",                 False, 0.001,    "m3"),
    0x4C: _ObjectSpec("gas_4",               False, 0.001,    "m3"),
    0x4D: _ObjectSpec("energy_4",            False, 0.001,    "kWh"),
    0x4E: _ObjectSpec("volume_precise",      False, 0.001,    "L"),
    0x4F: _ObjectSpec("water",               False, 0.001,    "L"),
    0x50: _ObjectSpec("timestamp",           False, 1,        None),
    0x51: _ObjectSpec("acceleration",        False, 0.001,    "m/s²"),
    0x52: _ObjectSpec("gyroscope",           False, 0.001,    "°/s"),
    0x55: _ObjectSpec("volume_storage",      False, 0.001,    "L"),
    0x56: _ObjectSpec("conductivity",        False, 1,        "µS/cm"),
    0x57: _ObjectSpec("temperature",         True,  1,        "C"),
    0x58: _ObjectSpec("temperature",         True,  0.35,     "C"),
    0x59: _ObjectSpec("count",               True,  1,        None),
    0x5A: _ObjectSpec("count",               True,  1,        None),
    0x5B: _ObjectSpec("count",               True,  1,        None),
    0x5C: _ObjectSpec("power",               True,  0.01,     "W"),
    0x5D: _ObjectSpec("current",             True,  0.001,    "A"),
    0x5E: _ObjectSpec("direction",           False, 0.01,     "°"),
    0x5F: _ObjectSpec("precipitation",       False, 0.1,      "mm"),
    0x60: _ObjectSpec("channel",             False, 1,        None),
    0x61: _ObjectSpec("rotational_speed",    False, 1,        "rpm"),
    0x62: _ObjectSpec("speed_signed",        True,  0.000001, "m/s"),
    0x63: _ObjectSpec("acceleration_signed", True,  0.000001, "m/s²"),
    0x64: _ObjectSpec("light_level",         False, 1,        None),
    0x65: _ObjectSpec("settings_revision",   False, 1,        None),

    # —— Boolean services —————————————————————————————————————————————————
    0x0F: _ObjectSpec("generic_boolean",     False, 1, None, is_bool=True),
    0x10: _ObjectSpec("power_binary",        False, 1, None, is_bool=True),
    0x11: _ObjectSpec("opening",             False, 1, None, is_bool=True),
    0x15: _ObjectSpec("battery_low",         False, 1, None, is_bool=True),
    0x16: _ObjectSpec("battery_charging",    False, 1, None, is_bool=True),
    0x17: _ObjectSpec("carbon_monoxide",     False, 1, None, is_bool=True),
    0x18: _ObjectSpec("cold",                False, 1, None, is_bool=True),
    0x19: _ObjectSpec("connectivity",        False, 1, None, is_bool=True),
    0x1A: _ObjectSpec("door",                False, 1, None, is_bool=True),
    0x1B: _ObjectSpec("garage_door",         False, 1, None, is_bool=True),
    0x1C: _ObjectSpec("gas_binary",          False, 1, None, is_bool=True),
    0x1D: _ObjectSpec("heat",                False, 1, None, is_bool=True),
    0x1E: _ObjectSpec("light_binary",        False, 1, None, is_bool=True),
    0x1F: _ObjectSpec("lock",                False, 1, None, is_bool=True),
    0x20: _ObjectSpec("moisture_binary",     False, 1, None, is_bool=True),
    0x21: _ObjectSpec("motion",              False, 1, None, is_bool=True),
    0x22: _ObjectSpec("moving",              False, 1, None, is_bool=True),
    0x23: _ObjectSpec("occupancy",           False, 1, None, is_bool=True),
    0x24: _ObjectSpec("plug",                False, 1, None, is_bool=True),
    0x25: _ObjectSpec("presence",            False, 1, None, is_bool=True),
    0x26: _ObjectSpec("problem",             False, 1, None, is_bool=True),
    0x27: _ObjectSpec("running",             False, 1, None, is_bool=True),
    0x28: _ObjectSpec("safety",              False, 1, None, is_bool=True),
    0x29: _ObjectSpec("smoke",               False, 1, None, is_bool=True),
    0x2A: _ObjectSpec("sound",               False, 1, None, is_bool=True),
    0x2B: _ObjectSpec("tamper",              False, 1, None, is_bool=True),
    0x2C: _ObjectSpec("vibration",           False, 1, None, is_bool=True),
    0x2D: _ObjectSpec("window",              False, 1, None, is_bool=True),

    # —— Events / commands / commands / raw (special) —————————————————————
    0x3A: _ObjectSpec("button_event",        False, 1, None),  # enum
    0x3B: _ObjectSpec("command",             False, 1, None),  # raw / variable length
    0x3C: _ObjectSpec("dimmer_event",        False, 1, "steps"),  # enum
    0x53: _ObjectSpec("text",                False, 1, None),  # variable length
    0x54: _ObjectSpec("raw",                 False, 1, None),  # variable length
}


class BTHomeV2Parser:
    @staticmethod
    def _decode_int(chunk: bytes, signed: bool) -> int:
        return int.from_bytes(chunk, byteorder="little", signed=signed)

    @staticmethod
    def parse(raw: bytes) -> list[ParsedMetric]:
        if len(raw) < 1:
            raise ValueError("Payload is empty")

        info_byte = raw[0]
        encrypted = bool(info_byte & 0x01)
        mac_included = bool(info_byte & 0x02)
        version = (info_byte >> 5) & 0x07

        if version != 2:
            raise ValueError(f"BTHome version unsupported: {version}")

        if encrypted:
            raise ValueError("Package is encrypted, skipped.")

        offset = 1
        if mac_included:
            if len(raw) < offset + 6:
                raise ValueError("mac_included=1, but MAC byte is empty.")
            offset += 6

        metrics: list[ParsedMetric] = []
        while offset < len(raw):
            object_id = raw[offset]
            offset += 1

            if object_id == _TEXT_OBJECT_ID:
                if offset >= len(raw):
                    break
                length = raw[offset]
                offset += 1
            else:
                length = LENGTH_TABLE.get(object_id)
                if length is None:
                    break

            chunk = raw[offset:offset + length]
            if len(chunk) < length:
                break
            offset += length

            spec = SEMANTIC_TABLE.get(object_id)
            if spec is None:
                continue

            if spec.is_bool:
                value: float | int | bool = bool(chunk[0])
            else:
                value = BTHomeV2Parser._decode_int(chunk, spec.signed) * spec.factor
                value = int(value) if spec.factor == 1 else round(value, 4)

            metrics.append(ParsedMetric(metric=spec.metric, value=value, unit=spec.unit))

        return metrics
