from enum import Enum

from pydantic import BaseModel, Field

from powerplant_challenge.schemas import Powerplant


class PowerplantFuelEnum(str, Enum):
    windturbine = "wind"
    gasfired = "gas"
    turbojet = "kerosine"
    # co2 = "co2"


class Prices(BaseModel):
    gas: float = Field(alias="gas(euro/MWh)", default=None)
    kerosine: float = Field(alias="kerosine(euro/MWh)", default=None)
    wind: float = Field(alias="wind(%)", default=None)
    co2: float = Field(alias="co2(euro/ton)", default=None)


class Productionplan(BaseModel):
    load: int
    fuels: Prices
    powerplants: list[Powerplant]


# Properties to return to client
class ProductionplanItemResponse(BaseModel):
    name: str
    p: float


class ProductionplanResponse(BaseModel):
    __root__: list[ProductionplanItemResponse]
