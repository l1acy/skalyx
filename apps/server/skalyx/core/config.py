import tomllib
from pathlib import Path

import tomlkit
from pydantic import BaseModel


class BleParserParams(BaseModel):
    service_data_uuid: str


class ConfigDevice(BaseModel):
    device_id: str
    address: str
    parser: str
    parser_params: BleParserParams


class SkalyxConfig(BaseModel):
    devices: list[ConfigDevice] = []


class Config:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, config_path: str = "skalyx.toml") -> None:
        self.load(config_path)

    def load(self, config_path: str = "skalyx.toml"):
        path = Path(config_path)

        if not path.exists():
            default_config = SkalyxConfig()
            config_dict = default_config.model_dump(exclude_none=True)

            toml_string = tomlkit.dumps(config_dict)
            path.write_text(toml_string, encoding="utf-8")

            self.__data = default_config
            return

        with open(config_path, "rb") as file:
            raw = tomllib.load(file)
        self.__data = SkalyxConfig.model_validate(raw)

    @property
    def data(self) -> SkalyxConfig:
        return self.__data
