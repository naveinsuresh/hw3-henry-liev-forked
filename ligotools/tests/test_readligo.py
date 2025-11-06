import readligo as rl
import numpy as np

import pytest

#accuarcy test
def test_loaddata():
    strain_h1, time_h1, chan_dict_h1 = rl.loaddata('data/H-H1_LOSC_4_V2-1126259446-32.hdf5', 'H1')
    assert np.isclose(strain_h1[1],2.08763900e-19)
    assert np.isclose(time_h1[1],1126259446.0002441)
    assert np.isclose(chan_dict_h1['CBC_CAT1'][1], 1)
    assert np.isclose(len(time_h1),131072)
    assert np.isclose(len(chan_dict_h1),13)
    strain_l1, time_l1, chan_dict_l1 = rl.loaddata('data/L-L1_LOSC_4_V2-1126259446-32.hdf5', 'L1')
    assert np.isclose(strain_l1[1], -1.03586274e-18)
    assert np.isclose(time_l1[1], 1.12625945e+09)
    assert np.isclose(chan_dict_l1['NO_CW_HW_INJ'].sum(),0)
    assert len(time_l1) == 131072
    assert len(chan_dict_l1) == 13

#type test
def test_type():
    strain_l1, time_l1, chan_dict_l1 = rl.loaddata('data/L-L1_LOSC_4_V2-1126259446-32.hdf5', 'L1')
    assert isinstance(strain_l1, np.ndarray)
    assert isinstance(time_l1,np.ndarray)
    assert isinstance(chan_dict_l1,dict)
    strain_h1, time_h1, chan_dict_h1 = rl.loaddata('data/H-H1_LOSC_4_V2-1126259446-32.hdf5', 'H1')
    assert isinstance(strain_h1, np.ndarray)
    assert isinstance(time_h1, np.ndarray)
    assert isinstance(chan_dict_h1, dict)