import pytest
from fpds import FPDS
import vcr


@vcr.use_cassette('fixtures/vcr_cassettes/fpds.yaml')
def test_get_data_from_fpds():
    d = FPDS().get_data_from_fpds(start_date="2016/01/01", end_date="2016/01/01")
    assert d
