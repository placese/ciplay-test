from decimal import DivisionByZero
from database import schemas
from fastapi.encoders import jsonable_encoder


def sort_statistics_list(statistics_obj_list: list[schemas.Statistics], sort: str) -> list[schemas.Statistics]:
    """Returns list statistics objects sorted by @sort"""
    return sorted(statistics_obj_list, key=lambda k: k[sort])


def calculate_CPC_and_CPM(statistics_obj_list: list[schemas.StatisticsBase]) -> list[schemas.Statistics]:
    """Returns list of statistics objects with CPC and CPM"""
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
        return round(cost / clicks, 2)
    except (DivisionByZero, ZeroDivisionError):
        return 0


def _calculate_CPM(cost: float, views: int) -> float:
    """Returns cost per millenium or returns 0 if number of views is 0"""
    try:
        return round((cost / views) * 1000, 2)
    except (DivisionByZero, ZeroDivisionError):
        return 0
