from pydantic import BaseModel


class ModuleHealth(BaseModel):
    module: str
    is_ok: bool
    message: str


SystemHealthResponse = list[ModuleHealth]
