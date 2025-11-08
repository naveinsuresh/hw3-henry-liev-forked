import numpy as np
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d
from ligotools import utils
import json
from scipy.io import wavfile
import os

def test_whiten():
    np.random.seed(0)
    strain = np.random.randn(1024)
    dt = 1.0 / 4096
    interp_psd = lambda f: np.ones_like(f)

    white_ht = utils.whiten(strain, interp_psd, dt)

    assert len(white_ht) == len(strain)
    assert np.isfinite(white_ht).all()
    assert abs(np.mean(white_ht)) < 1e-1
	
def test_write_wavfile(tmp_path):
    fs = 4096
    data = np.sin(2 * np.pi * 100 * np.linspace(0, 1, fs))
    filename = tmp_path / "test.wav"

    utils.write_wavfile(filename, fs, data)

    assert os.path.exists(filename)
    rate, read_data = wavfile.read(filename)

    assert rate == fs
    assert read_data.dtype == np.int16
    assert read_data.shape == data.shape


def test_reqshift():
    fs = 4096
    t = np.linspace(0, 1, fs, endpoint=False)
    f0 = 100
    signal = np.sin(2 * np.pi * f0 * t)

    shifted = utils.reqshift(signal, fshift=100, sample_rate=fs)

    assert len(shifted) == len(signal)
    assert not np.allclose(signal, shifted)
    assert np.isclose(np.std(signal), np.std(shifted), rtol=0.1)
