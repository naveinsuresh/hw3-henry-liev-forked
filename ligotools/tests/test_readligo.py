import numpy as np
import h5py
import pytest
from ligotools import readligo as rl


def test_dq_channel_to_seglist_basic():
    channel = np.array([0, 1, 1, 0, 1, 1, 1, 0])
    fs = 1  

    segs = rl.dq_channel_to_seglist(channel, fs=fs)

    expected = [slice(1, 3), slice(4, 7)]

    assert len(segs) == len(expected)
    for s, e in zip(segs, expected):
        assert s.start == e.start
        assert s.stop == e.stop



def test_loaddata(tmp_path):
    file_path = tmp_path / "tiny.hdf5"

    with h5py.File(file_path, "w") as f:
        strain = f.create_dataset("strain/Strain", data=np.array([0.1, 0.2, 0.3]))
        strain.attrs["Xspacing"] = 1.0 

        f.create_dataset("meta/GPSstart", data=1000000000)
        f.create_dataset("quality/simple/DQmask", data=np.array([1, 1, 1], dtype="int32"))
        f.create_dataset("quality/simple/DQShortnames", data=np.array([b"DATA"]))
        f.create_dataset("quality/injections/Injmask", data=np.array([0, 0, 0], dtype="int32"))
        f.create_dataset("quality/injections/InjShortnames", data=np.array([b"INJ"]))

    strain, time, dq = rl.loaddata(str(file_path))

    assert isinstance(strain, np.ndarray)
    assert isinstance(time, np.ndarray)
    assert isinstance(dq, dict)
    assert "DATA" in dq
    assert "INJ" in dq
    assert "DEFAULT" in dq
