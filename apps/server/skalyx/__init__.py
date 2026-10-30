from skalyx.adapters.ble_adapter import BleAdapter
from skalyx.core.bus import EventBus
from skalyx.core.storage import Storage

bus = EventBus()
ble_adapter = BleAdapter()
storage = Storage(bus)
