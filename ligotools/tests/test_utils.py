import numpy as np
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d
import readligo as rl
import utils
import json

def test_whiten():
    strain_l1, time_l1, chan_dict_l1 = rl.loaddata('data/L-L1_LOSC_4_V2-1126259446-32.hdf5', 'L1')
    eventname = 'GW150914' 
    events = json.load(open("data/BBH_events_v3.json","r"))
    event = events[eventname]
    fs = event['fs']                   
    NFFT = int(fs/8)
    Pxx_L1, freqs = mlab.psd(strain_l1, Fs = fs, NFFT = NFFT)
    psd_L1 = interp1d(freqs, Pxx_L1)

    strain_L1_whiten = utils.whiten(strain_l1,psd_L1,dt)
    
    assert abs(np.mean(strain_L1_whiten)) < 1e-3, "Whitened signal is not zero-mean"
    assert 0.5 < np.std(strain_L1_whiten) < 2.0, "Unexpected std for whitened signal"

def test_write_wavfile():
    data_test = np.arange(1, 2049)
    utils.write_wavfile("unit_test.wav", 4096, data_test)
    
    first_10_key = np.int16(data_test/np.max(np.abs(data_test)) * 32767 * 0.9)[:10]
    
    cdir = os.getcwd()
    f = wavfile.read(cdir + "/audio/unit_test.wav")
    
    assert type(f[1][:10]) == type(first_10_key), "Wrong Type"
    assert (f[1][:10] == first_10_key).all(), "Wrong Value"
    assert isinstance(f[0], (int, np.integer)), "Wrong Type"
    assert f[0] == 4096, "Wrong Value"
    
    os.remove(cdir + "/audio/unit_test.wav")

def test_reqshift():
    dt = 0.001
    strain_test = np.arange(1, 1000)
    Pxx_test, freqs_test = mlab.psd(strain_test, Fs = 4096, NFFT = 512)
    psd_test = interp1d(freqs_test, Pxx_test)
    whiten_test = whiten(strain_test, psd_test, dt)
    result = reqshift(whiten_test, fshift=1000, sample_rate=4096)
    
    first_10_key = np.array([-2790.36470897, 1023.42737067, 374.29757367, -992.00055018, 1010.37863495, 
                             -846.73870791, 745.83944289, -704.94183416, 653.34915656, -585.46202111])
    
    assert type(result[:10]) == type(first_10_key), "Wrong Type"
    assert np.allclose(result[:10], first_10_key), "Wrong Value"