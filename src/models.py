from typing import Optional
from pydantic import BaseModel, validator


class CreateBuilding(BaseModel):
    building: str
    level: int
    reserves: int = 1
    activate_production_methods: set[str]

    # def dict(self, *args, **kwargs):
    #     return {'create_building': self.dict()}

# class CultureId(str):
#     pass

# class ReligionId(str):
#     pass

# class StateId(str):
#     pass

# class CountryId(str):
#     pass

# class CreatePopDeclaration(BaseModel):
#     culture: CultureId
#     religion: Optional[ReligionId] = None
#     size: int

# class RegionStatePopDeclaration(BaseModel):
#     country_owning_region_state: CountryId
#     create_pop: CreatePopDeclaration

#     @validator('country_owning_region_state')
#     def add_prefix(cls, v):
#         return f'region_state:{v}'

# class StatePopDeclaration(BaseModel):
#     state: StateId
#     region_states: list[RegionStatePopDeclaration]

#     @validator('state')
#     def add_state_prefix(cls, v):
#         return f's:{v}'

# class PopsHistoryFile(BaseModel):
#     states_pops_declarations: list[StatePopDeclaration]

#     def dict(self, *args, **kwargs):
#         return {"POPS": self.states_pops_declarations}


class MapDataState(BaseModel):
    id: int
    provinces: list[str]
    capped_resources: dict[str, int] = {}
    traits: Optional[list[str]]
    arable_resources: Optional[list[str]]
    port: Optional[str]
    city: Optional[str]
    naval_exit_id: Optional[int]


# class CreateState:


# class StateHistory(BaseModel):
#     create_states: list[CreateState]


# class StateHistoryFile(BaseModel):
#     STATES: dict[str, StateHistory]
