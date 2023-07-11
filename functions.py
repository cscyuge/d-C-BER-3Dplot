import numpy as np
from scipy.special import lambertw, erfc, erfcinv
from config import *

def invW(x):
    return x*np.exp(x)


def invQ(x):
    return np.sqrt(2) * erfcinv(2 * x)

def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

def BER_SNR(BER):
    return 2*(invQ(BER)**2)

def C_SNR(C):
    return np.exp2(C/B)-1

def D_SNR(d):
    return (P_r * 2 * np.pi * (1 - np.cos(theta_1_e)) * (rho_t * rho_r) * (v**2)*(l**2) * (2/k * invW(k/2*d-n_i))**2) / (sigma_i**2 * r * np.cos(theta_i))


def calc_d_with_snr(snr):
    return 2/k*np.real(lambertw(k/2*np.sqrt(snr*(sigma_i**2)*r*np.cos(theta_i)/(P_r*2*np.pi*(1-np.cos(theta_1_e))*(rho_t*rho_r)*(v**2)*(l**2))))) + n_i

def calc_ber_with_snr(snr):
    return Q(np.sqrt(snr / 2))

def calc_C_with_snr(snr):
    return B * np.log2(1 + snr)