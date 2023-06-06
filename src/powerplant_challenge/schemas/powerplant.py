from enum import Enum
from pydantic import BaseModel


class PowerplantType(str, Enum):
    gasfired = "gasfired"
    windturbine = "windturbine"
    turbojet = "turbojet"


class Powerplant(BaseModel):
    name: str
    type: PowerplantType

    # the efficiency at which they convert a MWh of fuel into a MWh of electrical energy.
    # Wind-turbines do not consume 'fuel' and thus are considered to generate power at zero price.
    efficiency: float
    pmin: int
    pmax: int
