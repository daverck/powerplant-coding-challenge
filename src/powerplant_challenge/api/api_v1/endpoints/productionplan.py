from enum import Enum

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from powerplant_challenge.schemas.productionplan import (
    Productionplan,
    ProductionplanItemResponse, ProductionplanResponse, PowerplantFuelEnum
)

router = APIRouter()


@router.post("/", status_code=201, response_model=ProductionplanResponse)
def create_productionplan(
    *,
    productionplan_in: Productionplan,
) -> JSONResponse:
    """
    Create a new productionplan in the database.
    """
    remmaining_load = productionplan_in.load
    powerplant_chosen = []
    powerplants = []

    # compute effective power and price for each powerplant
    for p in productionplan_in.powerplants:
        if p.type == "windturbine":
            price_power_min = 0
            price_power_max = 0
            power_min = p.pmin*productionplan_in.fuels.__getattribute__(PowerplantFuelEnum[p.type].value)/100
            power_max = p.pmax*productionplan_in.fuels.__getattribute__(PowerplantFuelEnum[p.type].value)/100
        else:
            price_power_min = p.pmin*1/p.efficiency*productionplan_in.fuels.__getattribute__(PowerplantFuelEnum[p.type].value)
            price_power_max = p.pmax*1/p.efficiency*productionplan_in.fuels.__getattribute__(PowerplantFuelEnum[p.type].value)
            power_min = p.pmin
            power_max = p.pmax
        powerplants.append({
            "powerplant": p,
            "w_power_min": power_min,
            "w_power_max": power_max,
            "price_min": price_power_min,
            "price_max": price_power_max,
        })

    # sort powerplant by merit order
    class PowerplantMeritEnum(str, Enum):
        windturbine = 0
        gasfired = 1
        turbojet = 2
    powerplants.sort(key=lambda x: (PowerplantMeritEnum[x["powerplant"].type], -x["price_max"]))

    # todo: minimize cost with linear programming
    # objective function: minimize cost (fuel)
    #
    # inequalities constraints:
    # sum of p_max superior to desired load
    # desired load greater than smallest of p_min
    # price >= 0

    # pick powerplants for desired energy load
    for p in powerplants:
        if remmaining_load == 0:
            powerplant_chosen.append(
                ProductionplanItemResponse(
                    name=p["powerplant"].name,
                    p=0
                ))
        else:
            if p["w_power_min"] <= remmaining_load <= p["w_power_max"]:
                powerplant_chosen.append(
                    ProductionplanItemResponse(
                        name=p["powerplant"].name,
                        p=remmaining_load
                    ))
                remmaining_load = 0
            elif p["w_power_max"] <= remmaining_load:
                powerplant_chosen.append(
                    ProductionplanItemResponse(
                        name=p["powerplant"].name,
                        p=p["w_power_max"]
                    ))
                remmaining_load -= p["w_power_max"]
            elif remmaining_load <= p["w_power_min"]:
                powerplant_chosen.append(
                    ProductionplanItemResponse(
                        name=p["powerplant"].name,
                        p=0
                    ))

    return JSONResponse(content=jsonable_encoder(powerplant_chosen))

