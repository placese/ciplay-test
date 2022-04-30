from services.statistics_handler import (
    _calculate_CPC,
    _calculate_CPM,
    calculate_CPC_and_CPM,
    sort_statistics_list
)


def test_calculate_CPC():
    """Test case for _calculate_CPC function"""
    assert _calculate_CPC(5.0, 3) == 1.67
    assert _calculate_CPC(5.15, 0) == 0


def test_calculate_CPM():
    """Test case for _calculate_CPM function"""
    assert _calculate_CPM(5.0, 10) == 500
    assert _calculate_CPM(5.0, 0) == 0


def test_calculate_CPC_and_CPM(get_statistics_before_list, get_expected_statistics_list):
    """Test case for calculate_CPC_and_CPM function"""
    assert calculate_CPC_and_CPM(get_statistics_before_list) == get_expected_statistics_list


def test_sort_statistics_list(get_expected_statistics_list):
    """Test case fpr sort_statistics_list function"""
    expected_statistics = sorted(get_expected_statistics_list, key=lambda k: k['cpc'])
    assert sort_statistics_list(statistics_obj_list=get_expected_statistics_list, sort='cpc') == expected_statistics
