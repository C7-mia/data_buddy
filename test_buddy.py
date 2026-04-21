import data_buddy


def test_basic_stat_functions():
    scores = [85, 90, 78, 92, 88, 500]

    assert round(data_buddy.get_average(scores), 2) == 155.5
    assert data_buddy.get_median(scores) == 89.0
    assert data_buddy.get_min(scores) == 78.0
    assert data_buddy.get_max(scores) == 500.0
