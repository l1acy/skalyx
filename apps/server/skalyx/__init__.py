from skalyx.adapters.ble_adapter import BleAdapter
from skalyx.adapters.http_adapter import HTTPAdapter
from skalyx.core.bus import EventBus
from skalyx.core.storage import Storage

bus = EventBus()
ble_adapter = BleAdapter()
http_adapter = HTTPAdapter()
storage = Storage(bus)
