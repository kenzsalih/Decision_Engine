import pytest
from engine.normalization import Normalizer


def test_benefit_normalization_basic():
    values = [10, 20, 30]
    result = Normalizer.normalize_numeric(values, "benefit")

    assert result == [0.0, 0.5, 1.0]


def test_cost_normalization_basic():
    values = [10, 20, 30]
    result = Normalizer.normalize_numeric(values, "cost")

    assert result == [1.0, 0.5, 0.0]


def test_edge_case_no_variance():
    values = [50, 50, 50]
    result = Normalizer.normalize_numeric(values, "benefit")

    assert result == [1.0, 1.0, 1.0]


def test_empty_values():
    values = []
    result = Normalizer.normalize_numeric(values, "benefit")

    assert result == []


def test_invalid_criterion_type():
    values = [1, 2, 3]

    with pytest.raises(ValueError):
        Normalizer.normalize_numeric(values, "invalid_type")


def test_precision_rounding():
    values = [1, 2, 4]  
    # benefit normalization:
    # min = 1, max = 4
    # results = [0.0, 0.333333..., 1.0]
    result = Normalizer.normalize_numeric(values, "benefit")

    assert result[1] == 0.333333
    assert len(str(result[1]).split(".")[1]) <= 6


def test_output_range_bounds():
    values = [5, 15, 25, 35]
    result = Normalizer.normalize_numeric(values, "benefit")

    for utility in result:
        assert 0.0 <= utility <= 1.0