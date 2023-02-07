from pydantic import BaseModel

class CreateBuilding(BaseModel):
    building: str
    level: int
    reserves: int = 1
    activate_production_methods: set[str]