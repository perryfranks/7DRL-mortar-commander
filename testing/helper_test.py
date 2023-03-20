import pytest
import helper


def test_two_point_distance_zero():
    x1 = x2 = y1 = y2 = 0
    xy1 = x1, y1
    xy2 = x2, y2

    assert helper.two_point_distance(xy1, xy2) == 0
