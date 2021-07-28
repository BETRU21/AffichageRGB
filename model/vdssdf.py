import numpy as np
wavelength = np.array([785, 786, 788, 789])



def returnWaveNumber(laser):
    waveNumber = ((1 / laser) - (1 / wavelength)) * 10 ** 7
    return waveNumber.round(0)


allo = returnWaveNumber(785)
print(allo)
print(np.array([0., 16., 48., 65.]))