from decimal import DivisionByZero
from database import crud, schemas
from fastapi.encoders import jsonable_encoder


def calculate_CPC_and_CPM(statistics_obj_list: list[schemas.StatisticsBase]) -> schemas.Statistics:
    """Returns statistics object with CPC and CPM"""
    statistics_json_list = []
    for statistics_obj in statistics_obj_list:
        statistics_obj = jsonable_encoder(statistics_obj)
        statistics_obj['cpc'] = _calculate_CPC(cost=statistics_obj.get('cost'), clicks=statistics_obj.get('clicks'))
        statistics_obj['cpm'] = _calculate_CPM(cost=statistics_obj.get('cost'), views=statistics_obj.get('views'))
        statistics_json_list.append(statistics_obj)
    return statistics_json_list


def _calculate_CPC(cost: float, clicks: int) -> float:
    """Returns cost per click or returns 0 if number of clicks is 0"""
    try:
        return cost / clicks
    except (DivisionByZero, ZeroDivisionError) as e:
        return 0


def _calculate_CPM(cost: float, views: int) -> float:
    """Returns cost per millenium or returns 0 if number of views is 0"""
    try:
        return cost / views * 1000
    except (DivisionByZero, ZeroDivisionError) as e:
        return 0
